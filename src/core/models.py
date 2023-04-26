import decimal

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class PersonalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.first_name}"


class Category(models.Model):
    title = models.CharField(max_length=120, db_index=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self) -> str | None:
        """getting url of category by slug"""
        return reverse("product_list_by_category", kwargs={"category_slug": self.slug})


class Product(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    description = models.TextField()
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_exists = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self) -> str | None:
        """getting url of product by id"""
        return reverse("product_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        return f"{self.first_name}'s order"

    def get_total_cost(self) -> decimal.Decimal:
        """Get total cost of order"""
        return sum(item.get_cost() for item in self.items.all())

    def get_items_flat(self):
        """Get order items summary"""
        return (item for item in self.items.select_related("product").all())

    def get_absolute_url(self) -> str | None:
        """Get url of order by order id"""
        return reverse("order_detail", kwargs={"pk": self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.DecimalField(max_digits=18, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def __str__(self) -> str:
        return f"Order Item <{self.product.title}>"

    def get_cost(self) -> decimal.Decimal:
        """Getting cost of order item (multiple of order item price to quantity of item)"""
        return self.quantity * self.price
