from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from shipments.helpers.helper import get_24_char_uuid


class SellerDetails(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=24, primary_key=True, default=get_24_char_uuid)
    name = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    client_secret = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10)
    access_token = models.CharField(max_length=1000, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'client_id', 'client_secret']

    objects = BaseUserManager()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return '{} {}'.format(self.id, self.name)

    class Meta:
        verbose_name = 'Seller detail'


class CustomerDetails(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=get_24_char_uuid)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.id)

    class Meta:
        verbose_name = 'Customer detail'


class ShipmentDetails(models.Model):
    STATUS_TYPE_PENDING = 'PENDING'
    STATUS_TYPE_PROCESSED = 'PROCESSED'

    status_type_choices = ((STATUS_TYPE_PENDING, STATUS_TYPE_PENDING),
                           (STATUS_TYPE_PROCESSED, STATUS_TYPE_PROCESSED))

    id = models.CharField(max_length=24, primary_key=True, default=get_24_char_uuid)
    shipment_id = models.IntegerField(unique=True)
    shipment_date = models.DateTimeField()
    transport_id = models.CharField(max_length=30, unique=True)
    transport_label = models.CharField(max_length=15, blank=True, null=True)
    shipment_reference = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=status_type_choices, default=STATUS_TYPE_PENDING)
    seller = models.ForeignKey(SellerDetails, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomerDetails, on_delete=models.DO_NOTHING, blank=True, null=True)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return '{} {}'.format(self.shipment_id, self.shipment_reference)

    class Meta:
        verbose_name = 'Shipment detail'


class OrderItem(models.Model):
    id = models.CharField(max_length=24, primary_key=True, default=get_24_char_uuid)
    order_id = models.CharField(max_length=30, unique=True)
    order_item_id = models.CharField(max_length=30)
    order_date = models.DateTimeField()
    name = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    order_condition = models.CharField(max_length=30, blank=True, null=True)
    fulfilment_method = models.CharField(max_length=3)
    shipment = models.ForeignKey(ShipmentDetails, on_delete=models.DO_NOTHING)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return '{} {}'.format(self.name, self.order_id)

    class Meta:
        verbose_name = 'Order detail'

