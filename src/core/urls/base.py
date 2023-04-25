from django.urls import include, path

from ..views import LoginView, RegisterView
from .shop import urlpatterns as shop_urlpatterns

urlpatterns = [
    path("shop/", include(shop_urlpatterns)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
