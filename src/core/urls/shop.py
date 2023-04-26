from django.urls import path

from ..views import CartView, checkout_history, product_detail, product_list

urlpatterns = [
    path("product/<int:pk>/", product_detail, name="product_detail"),
    path("checkout-history/", checkout_history, name="checkout_history"),
    path("cart/", CartView.as_view(), name="cart"),
    path("<slug:category_slug>/", product_list, name="product_list_by_category"),
    path("", product_list, name="product_list"),
]
