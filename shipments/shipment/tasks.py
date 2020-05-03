import time

from shipments.celery.celery import app
from shipments.seller.seller import BolooSellerDetails
from shipments.shipment.shipment import BolooShipmentDetails


@app.task
def get_all_shipments(seller_id):
    seller = BolooSellerDetails.get_seller_by_id(seller_id)
    BolooShipmentDetails(seller=seller).get_all_shipments_from_bol_by_fulfilment_method('FBR')
    BolooShipmentDetails(seller=seller).get_all_shipments_from_bol_by_fulfilment_method('FBB')
    update_pending_shipments.delay(seller_id)


@app.task
def update_pending_shipments(seller_id, shipments=None):
    seller = BolooSellerDetails.get_seller_by_id(seller_id)
    if not shipments:
        shipments = BolooShipmentDetails(seller=seller).get_pending_shipments_by_seller()

    shipment_ids = list(shipments.values_list('shipment_id', flat=True))
    for shipment_id in shipment_ids:
        update_pending_shipment.delay(seller_id, shipment_id)


@app.task
def update_pending_shipment(seller_id, shipment_id):
    retry = 1
    seller = BolooSellerDetails.get_seller_by_id(seller_id)
    status, message = BolooShipmentDetails(seller=seller,
                                           shipment_id=shipment_id).get_and_update_shipment_details_from_bol()
    if status == -1:
        BolooSellerDetails(seller=seller).create_access_token()
        seller.refresh_from_db()
        update_pending_shipment.delay(seller.id, shipment_id)

    if status == -2:
        time.sleep(60)
        if retry == 3:
            return None

        retry += 1


