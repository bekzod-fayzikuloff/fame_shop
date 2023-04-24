"""
Customize admin panel for models
"""

from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("title",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("title", "description", "category__title")
    list_filter = ("price", "category")
    list_display = ("title",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ("email", "first_name", "city", "last_name")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ("product__title", "product__description", "order__email", "order__first_name")
