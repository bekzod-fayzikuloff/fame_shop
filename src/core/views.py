import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms.orders import CreateOrderForm
from .forms.users import CreateUserForm, UserPersonalDataForm
from .models import Category, Order, OrderItem, PersonalData, Product
from .services import get_personal_data_initial, is_authenticated


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


@login_required
def checkout_history(request: HttpRequest) -> HttpResponse:
    """View orders history for login user"""
    orders = Order.objects.filter(email=request.user.email)
    return render(request, "shops/checkout_history.html", context={"orders": orders})


def logout_view(request: HttpRequest) -> HttpResponse:
    """Logout handling"""
    logout(request)
    return redirect("product_list")


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        """Profile personal data page"""
        initial = get_personal_data_initial(self.request.user)
        form = UserPersonalDataForm(initial=initial)
        return render(self.request, "users/profile.html", context={"form": form})

    @method_decorator(login_required)
    def post(self, request: HttpRequest) -> HttpResponse:
        """Handling profile personal data changing"""
        form = UserPersonalDataForm(self.request.POST)
        if form.is_valid():
            if PersonalData.objects.filter(user=self.request.user).exists():
                for field in form.cleaned_data:
                    setattr(self.request.user.personaldata, field, form.cleaned_data[field])
                self.request.user.personaldata.save()
            else:
                form.cleaned_data["user"] = self.request.user
                PersonalData.objects.create(**form.cleaned_data)

            return redirect("product_list")
        messages.error(request, "Unsuccessful registration. Check provide credential")
        return render(self.request, "users/register.html", context={"form": form})


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


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get login page"""
        form = AuthenticationForm()
        return render(self.request, "users/login.html", context={"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Handling User login"""
        is_auth, user = is_authenticated(request)

        if is_auth:
            login(request, user)
            return redirect("product_list")

        messages.error(request, "Unsuccessful login. Check provide credential")
        form = AuthenticationForm()
        return render(self.request, "users/login.html", context={"form": form})


class CartView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Get cart from cookie and render cart page"""
        cart = request.COOKIES.get("cart")
        cart_content = []
        if cart and (cart_obj := json.loads(cart)):
            for item in cart_obj:
                product = Product.objects.get(pk=item.get("productId"))
                item_quantity = item.get("quantity")
                # Add auxiliary fields
                cart_content.append(
                    {"product": product, "quantity": item_quantity, "total": product.price * item_quantity}
                )

            total_cost = sum(map(lambda x: x.get("total"), cart_content))
        else:
            cart_content = []
            total_cost = 0

        initial = get_personal_data_initial(self.request.user)
        form = CreateOrderForm(initial=initial)
        return render(
            self.request, "shops/cart.html", context={"cart": cart_content, "total_cost": total_cost, "form": form}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        """Cart items checkout"""
        form = CreateOrderForm(self.request.POST)
        cart = request.COOKIES.get("cart")

        if form.is_valid():
            order = form.save()
            if cart and (cart_obj := json.loads(cart)):
                execute_entry = []
                for item in cart_obj:
                    product = Product.objects.get(pk=item.get("productId"))
                    execute_entry.append(
                        OrderItem(order=order, product=product, price=product.price, quantity=item.get("quantity"))
                    )
                OrderItem.objects.bulk_create(execute_entry)  # Create db records by one query

                messages.success(request, "Checkout was completed successfully")
                return render(self.request, "shops/cart.html", context={"form": form})

        messages.error(request, "Checkout was failed. You need peek any item")
        return render(self.request, "shops/cart.html", context={"form": form})
