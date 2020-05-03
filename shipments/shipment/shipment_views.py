from rest_framework.decorators import api_view

from shipments.helpers.decorators import validate_user
from shipments.helpers.paginator import BolooPaginator
from shipments.helpers.result_builder import ResultBuilder
from shipments.shipment.shipment import BolooShipmentDetails
from shipments.shipment.tasks import get_all_shipments


@api_view(['GET'])
@validate_user
def api_get_all_shipments(request):
    result_builder = ResultBuilder()
    get_data = request.GET

    page_number = get_data.get('page', 1)
    shipments = BolooShipmentDetails(seller=request.user).get_all_shipments_by_seller()
    if not shipments:
        return result_builder.ok_200().fail().message('No shipments for the seller').get_response()

    boloo_paginator = BolooPaginator(data=shipments, page_size=25)
    status, message, shipments = boloo_paginator.get_page(page_number)
    if status == 0:
        return result_builder.ok_200().fail().message(message).get_response()

    serialized_shipments = BolooShipmentDetails().get_serialized_shipments(shipments)
    return result_builder.success().message('Shipment fetched').result_object(serialized_shipments).get_response()


@api_view(['POST'])
@validate_user
def api_initiate_shipment_sync(request):
    result_builder = ResultBuilder()
    get_all_shipments.delay(request.user.id)
    return result_builder.success().message('Sync has started. Shipments will be available soon').get_response()

