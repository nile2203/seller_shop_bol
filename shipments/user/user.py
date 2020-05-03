import json

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from shipments.models import CustomerDetails


class BolooShipmentCustomerDetails:
    def __init__(self, user=None):
        self.user = user

    def get_serialized_user(self):
        if not self.user:
            return None

        return BolooShipmentCustomerDetailsSerializer.get_serialized(self.user)

    @staticmethod
    def create_user(user_detail):
        '''
          {'salutationCode': '03',
           'zipCode': '2215DJ',
           'countryCode': 'NL'}
        '''
        if not isinstance(user_detail, dict):
            return None

        CustomerDetails.objects.create(
            first_name=user_detail.get('first_name'), last_name=user_detail.get('last_name'),
            pin_code=user_detail.get('zipCode'), city=user_detail.get('city'), email=user_detail.get('email'),
            phone_number=user_detail.get('deliveryPhoneNumber'))


class BolooShipmentCustomerDetailsSerializer(serializers.ModelSerializer):
    @staticmethod
    def get_serialized(user):
        data = BolooShipmentCustomerDetailsSerializer(user).data
        return json.loads(JSONRenderer().render(data))

    class Meta:
        model = CustomerDetails
        exclude = ['created', 'modified']
