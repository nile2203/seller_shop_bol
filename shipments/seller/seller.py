import json

from shipments.accessor.boloo import BolooAccessor
from shipments.models import SellerDetails


class BolooSellerDetails:
    def __init__(self, seller):
        self.seller = seller

    @staticmethod
    def check_and_get_seller_by_client_credentials(client_id, client_secret):
        seller_details = SellerDetails.objects.filter(client_id=client_id, client_secret=client_secret).first()
        if not seller_details:
            return 0, 'Invalid credentials', None

        return 1, 'Valid credentials', seller_details

    def get_access_token(self):
        status, message, content = BolooAccessor().get_access_token(client_id=self.seller.client_id,
                                                                           client_secret=self.seller.client_secret)
        if status == 0:
            return 0, message, None

        content = json.loads(content.decode('utf-8'))
        return 1, 'Authorization token fetched', content['access_token']

