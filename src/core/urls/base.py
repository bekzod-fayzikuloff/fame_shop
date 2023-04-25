from django.urls import include, path

from .shop import urlpatterns as shop_urlpatterns

urlpatterns = [path("shop/", include(shop_urlpatterns))]
