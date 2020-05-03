from django.conf.urls import url

from shipments.seller import seller_views
from shipments.shipment import shipment_views

urlpatterns = [
    url(r'v1/access/token/create/', seller_views.api_create_access_token),

    url(r'v1/shipments/all/', shipment_views.api_get_all_shipments),
    url(r'v1/shipments/sync/initiate/', shipment_views.api_initiate_shipment_sync)
]