from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms.users import CreateUserForm
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


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get register page"""
        form = CreateUserForm()
        return render(self.request, "users/register.html", context={"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """New user create handling `validate and redirect`"""
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            user = form.save()
            login(self.request, user)
            return redirect("product_list")
        messages.error(request, "Unsuccessful registration. Check provide credential")
        return render(self.request, "users/register.html", context={"form": form})
