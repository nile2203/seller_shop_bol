from django.db.models.query import QuerySet

from shipments.celery.celery import app
from shipments.helpers.constants import FULFILMENT_METHODS
from shipments.seller.seller import BolooSellerDetails
from shipments.shipment.shipment import BolooShipmentDetails


@app.task
def get_all_shipments():
    sellers = BolooSellerDetails.get_all_seller_details()
    for seller in sellers:
        get_all_shipments_for_seller.delay(seller.id)


@app.task
def get_all_shipments_for_seller(seller_id):
    seller = BolooSellerDetails.get_seller_by_id(seller_id)
    boloo_seller = BolooShipmentDetails(seller=seller)

    for fulfilment_method in FULFILMENT_METHODS:
        status, message, content = boloo_seller.get_all_shipments_from_bol_by_fulfilment_method(
            fulfilment_method=fulfilment_method)
        if status == 1 and not content:
            continue

        if status in [0, -4, -5]:
            print(message)
            # Ideally some kind of email system to inform developers about the failure
            return

        if status == -2:
            get_all_shipments_for_seller.apply_async([seller_id], countdown=70)
            return

    update_pending_shipments.delay(seller_id)


@app.task
def update_pending_shipments(seller_id, shipments=None):
    if not shipments:
        shipments = BolooShipmentDetails(seller_id=seller_id).get_pending_shipments_by_seller()

    if not isinstance(shipments, QuerySet):
        # Internal email or some tracking service should be called to register such inconsistency
        return

    shipment_ids = list(shipments.values_list('shipment_id', flat=True))
    for shipment_id in shipment_ids:
        update_pending_shipment.delay(seller_id, shipment_id)


@app.task
def update_pending_shipment(seller_id, shipment_id):
    seller = BolooSellerDetails.get_seller_by_id(seller_id)
    status, message = BolooShipmentDetails(
        seller=seller, shipment_id=shipment_id).get_and_update_shipment_details_from_bol()
    if status == -1:
        BolooSellerDetails(seller=seller).create_access_token()
        update_pending_shipment.apply_async([seller_id, shipment_id], countdown=10)
        return

    if status == -2:
        update_pending_shipment.apply_async([seller_id, shipment_id], countdown=70)
        return

    if status in [0, -4, -5]:
        print(message)
        # Ideally some kind of email system to inform developers about the failure
        return
