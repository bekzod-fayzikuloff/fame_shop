from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request: HttpRequest, category_slug=None) -> HttpResponse:
    """List of all products or filter by category handler"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_exists=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    return render(request, "shops/list.html", {"category": category, "categories": categories, "products": products})


def product_detail(request: HttpRequest, pk) -> HttpResponse:
    """Product detail handler"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shops/detail.html", context={"product": product})
