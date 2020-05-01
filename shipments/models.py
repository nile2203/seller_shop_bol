from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from shipments.helpers.helper import get_24_char_uuid


class SellerDetails(AbstractBaseUser, PermissionsMixin):
    seller_id = models.CharField(max_length=24, primary_key=True, default=get_24_char_uuid)
    name = models.CharField(max_length=50)
    client_id = models.CharField(max_length=50)
    client_secret = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'client_id', 'client_secret']

    objects = BaseUserManager()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return '{} {}'.format(self.seller_id, self.name)

    class Meta:
        verbose_name = 'Seller detail'

