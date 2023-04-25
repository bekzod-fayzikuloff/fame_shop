from django.urls import include, path

from ..views import RegisterView
from .shop import urlpatterns as shop_urlpatterns

urlpatterns = [path("shop/", include(shop_urlpatterns)), path("register/", RegisterView.as_view())]
