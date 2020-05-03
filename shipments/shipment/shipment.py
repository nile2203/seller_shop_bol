import json
import time

from django.db import IntegrityError
from django.db import transaction as db_transaction

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from shipments.accessor.boloo import BolooAccessor
from shipments.helpers.helper import format_datetime_user_friendly
from shipments.models import ShipmentDetails
from shipments.order.order import BolooShipmentOrderDetails
from shipments.seller.seller import BolooSellerDetails
from shipments.user.user import BolooShipmentCustomerDetails


class BolooShipmentDetails:
    def __init__(self, shipment_id=None, shipment=None, seller=None):
        self.shipment_id = shipment_id
        self.shipment = shipment
        self.seller = seller

    def get_shipment_by_shipment_id(self):
        return ShipmentDetails.objects.filter(shipment_id=self.shipment_id).select_related('seller', 'user').first()

    def get_all_shipments_by_seller(self):
        return ShipmentDetails.objects.filter(status=ShipmentDetails.STATUS_TYPE_PROCESSED,
                                              seller=self.seller).select_related('seller', 'user')

    def get_serialized_shipment(self):
        if not self.shipment:
            return None

        return BolooShipmentDetailsSerializer.get_serialized(self.shipment)

    def get_serialized_shipments(self, shipments):
        if not isinstance(shipments, list):
            return None

        serialized_shipments = []
        for shipment in shipments:
            self.shipment = shipment
            serialized_shipment = self.get_serialized_shipment()
            if not serialized_shipment:
                continue

            serialized_shipments.append({
                'shipment': serialized_shipment,
                'orders': BolooShipmentOrderDetails.get_serialized_orders(self.shipment.orderitem_set.all()),
                'user': BolooShipmentCustomerDetails(user=self.shipment.user).get_serialized_user()
                if self.shipment.user else dict()
            })

        return serialized_shipments

    def get_pending_shipments_by_seller(self):
        return ShipmentDetails.objects.filter(status=ShipmentDetails.STATUS_TYPE_PENDING,
                                              seller=self.seller).select_related('user', 'seller')[:5]

    def create_shipment_details(self, content):
        shipments = content.get('shipments')
        if not shipments:
            return None

        '''
        [{'shipmentId': 720390093, 'shipmentDate': '2020-02-16T00:37:19+01:00',
         'shipmentReference': '081234501144565966',
         'shipmentItems': [{'orderItemId': 'BFC0000368844210', 'orderId': '2887647170'}],
         'transport': {'transportId': 460679758}}]
        '''
        shipment_object_list = []
        for shipment in shipments:
            shipment_object_list.append(ShipmentDetails(
                shipment_id=shipment['shipmentId'], shipment_reference=shipment.get('shipmentReference'),
                shipment_date=shipment['shipmentDate'], transport_id=shipment.get('transport').get('transportId'),
                seller=self.seller))

        try:
            ShipmentDetails.objects.bulk_create(shipment_object_list)
        except IntegrityError:
            pass

    def get_all_shipments_from_bol_by_fulfilment_method(self, fulfilment_method):
        boloo_accessor = BolooAccessor(access_token=self.seller.access_token)
        boloo_seller = BolooSellerDetails(seller=self.seller)
        retry, page_number = 1, 1
        while True:
            status, message, content = boloo_accessor.get_all_shipments(
                page_number=page_number, fulfilment_method=fulfilment_method)
            print(content, status, message)
            if status == -1:
                boloo_seller.create_access_token()
                boloo_seller.seller.refresh_from_db()
                boloo_accessor.access_token = boloo_seller.seller.access_token
                continue

            if status == -2:
                time.sleep(60)
                if retry == 3:
                    break

                retry += 1
                continue

            if status == 0:
                continue

            if not content:
                break

            self.create_shipment_details(content)
            page_number += 1

    def update_shipment_details(self, content):
        '''
        {'shipmentId': 720390093,
          'pickUpPoint': False,
          'shipmentDate': '2020-02-16T00:37:19+01:00',
          'shipmentReference': '081234501144565966',
          'shipmentItems': [{'orderItemId': 'BFC0000368844210',
            'orderId': '2887647170',
            'orderDate': '2020-02-15T22:29:17+01:00',
            'latestDeliveryDate': '2020-02-17T00:00:00+01:00',
            'ean': '8719326544885',
            'title': 'XXL Gaming Muismat - Grote Bureau Onderlegger - Antislip - Mousepad - 90 x 40 cm - Wereldkaart',
            'quantity': 1,
            'offerPrice': 20.0,
            'offerCondition': 'NEW',
            'fulfilmentMethod': 'FBB'}],
          'transport': {'transportId': 460679758,
           'transporterCode': 'TNT',
           'trackAndTrace': '3STUNM066560102'},
          'customerDetails': {'salutationCode': '03',
           'zipCode': '2215DJ',
           'countryCode': 'NL'}}
        '''
        if not content:
            return None

        with db_transaction.atomic():
            self.shipment = self.get_shipment_by_shipment_id()
            BolooShipmentOrderDetails(shipment=self.shipment).create_orders(content.get('shipmentItems'))
            BolooShipmentCustomerDetails.create_user(content.get('customerDetails'))
            self.shipment.status = ShipmentDetails.STATUS_TYPE_PROCESSED
            self.shipment.save()

    def get_and_update_shipment_details_from_bol(self):
        boloo_accessor = BolooAccessor(access_token=self.seller.access_token)
        status, message, content = boloo_accessor.get_shipment_details(self.shipment_id)
        if status == 1:
            self.update_shipment_details(content)
            return 1, 'Shipment details updated'

        return status, message


class BolooShipmentDetailsSerializer(serializers.ModelSerializer):
    shipment_date_formatted = serializers.SerializerMethodField()

    def get_shipment_date_formatted(self, shipment):
        return format_datetime_user_friendly(shipment.shipment_date)

    @staticmethod
    def get_serialized(shipment):
        data = BolooShipmentDetailsSerializer(shipment).data
        return json.loads(JSONRenderer().render(data))

    class Meta:
        model = ShipmentDetails
        fields = ['id', 'shipment_id', 'shipment_date_formatted', 'transport_id', 'transport_label',
                  'shipment_reference']
