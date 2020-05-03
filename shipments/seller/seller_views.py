from rest_framework.decorators import api_view

from shipments.helpers.result_builder import ResultBuilder
from shipments.seller.seller import BolooSellerDetails


@api_view(['POST'])
def api_create_access_token(request):
    result_builder = ResultBuilder()
    post_data = request.data

    client_id = post_data.get('client_id')
    client_secret = post_data.get('client_secret')
    if not (client_id and client_secret):
        return result_builder.bad_request_400().fail().message('Client credentials not provided').get_response()

    status, message, seller_details = BolooSellerDetails.check_and_get_seller_by_client_credentials(
        client_id=client_id, client_secret=client_secret)
    if status == 0:
        return result_builder.ok_200().fail().message(message).get_response()

    boloo_seller = BolooSellerDetails(seller=seller_details)
    status, message, auth_token = boloo_seller.create_access_token()
    if status == 0:
        return result_builder.ok_200().fail().message(message).get_response()

    result = {
        'auth_token': auth_token
    }
    return result_builder.ok_200().success().result_object(result).message(message).get_response()
