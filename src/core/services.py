from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpRequest


def is_authenticated(request: HttpRequest) -> tuple[bool, User | None]:
    """Check provide request user is authenticated"""
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            return True, user
    return False, None


def get_personal_data_initial(user: User) -> dict | None:
    if hasattr(user, "personaldata"):
        p_data = user.personaldata
        initial = {
            "first_name": p_data.first_name,
            "last_name": p_data.last_name,
            "address": p_data.address,
            "postal_code": p_data.postal_code,
            "city": p_data.city,
            "phone_number": p_data.phone_number,
        }
    else:
        initial = None

    return initial
