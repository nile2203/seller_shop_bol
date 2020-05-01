from django.conf.urls import url

from shipments.seller import seller_views

urlpatterns = [
    url(r'v1/access/token/get/', seller_views.api_get_access_token)
]