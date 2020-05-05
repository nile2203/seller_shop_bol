import json

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from shipments.helpers.helper import format_datetime_user_friendly
from shipments.models import OrderItem


class BolooShipmentOrderDetails:
    def __init__(self, order=None, shipment=None):
        self.shipment = shipment
        self.order = order

    def get_serialized_order(self):
        if not self.order:
            return None

        return BolooShipmentOrderDetailsSerializer.get_serialized(self.order)

    @staticmethod
    def get_serialized_orders(orders):
        return BolooShipmentOrderDetailsSerializer.get_serialized(orders, many=True)

    def create_orders(self, order_details):
        '''
        [{'orderItemId': 'BFC0000368844210',
            'orderId': '2887647170',
            'orderDate': '2020-02-15T22:29:17+01:00',
            'latestDeliveryDate': '2020-02-17T00:00:00+01:00',
            'ean': '8719326544885',
            'title': 'XXL Gaming Muismat - Grote Bureau Onderlegger - Antislip - Mousepad - 90 x 40 cm - Wereldkaart',
            'quantity': 1,
            'offerPrice': 20.0,
            'offerCondition': 'NEW',
            'fulfilmentMethod': 'FBB'}]
        '''
        if not isinstance(order_details, list):
            return None

        order_object_list = []
        for order_detail in order_details:
            order_object_list.append(OrderItem(
                order_id=order_detail['orderId'], order_item_id=order_detail['orderItemId'],
                order_date=order_detail['orderDate'], name=order_detail['title'], quantity=order_detail['quantity'],
                price=order_detail['offerPrice'], order_condition=order_detail.get('offerCondition'),
                fulfilment_method=order_detail['fulfilmentMethod'], shipment=self.shipment))

        OrderItem.objects.bulk_create(order_object_list, ignore_conflicts=True)


class BolooShipmentOrderDetailsSerializer(serializers.ModelSerializer):
    order_date_formatted = serializers.SerializerMethodField()

    def get_order_date_formatted(self, order):
        return format_datetime_user_friendly(order.order_data)

    @staticmethod
    def get_serialized(order, many=False):
        data = BolooShipmentOrderDetailsSerializer(order, many=many).data
        return json.loads(JSONRenderer().render(data))

    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'order_date_formatted', 'order_item_id', 'name', 'quantity', 'price',
                  'order_condition', 'fulfilment_method']