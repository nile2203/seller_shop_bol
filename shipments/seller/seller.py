from django.db import IntegrityError
from rest_framework.authtoken.models import Token

from shipments.accessor.boloo import BolooAccessor
from shipments.models import SellerDetails


class BolooSellerDetails:
    def __init__(self, seller):
        self.seller = seller

    @staticmethod
    def get_seller_by_id(seller_id):
        return SellerDetails.objects.filter(id=seller_id).first()

    @staticmethod
    def check_and_get_seller_by_client_credentials(client_id, client_secret):
        seller_details = SellerDetails.objects.filter(client_id=client_id, client_secret=client_secret).first()
        if not seller_details:
            return 0, 'Invalid credentials', None

        return 1, 'Valid credentials', seller_details

    def create_access_token(self):
        status, message, content = BolooAccessor().get_access_token(client_id=self.seller.client_id,
                                                                    client_secret=self.seller.client_secret)
        print(status, message, content)
        if status == 0:
            return 0, message, None

        token, created = Token.objects.get_or_create(user=self.seller)

        self.seller.access_token = content['access_token']
        self.seller.save()
        return 1, 'Authorization token fetched', token.key

    @staticmethod
    def get_all_seller_details():
        return SellerDetails.objects.filter().order_by('-created')
