from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

User = settings.AUTH_USER_MODEL


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.street}, {self.city}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.pk} for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey("catalog.MenuItem", on_delete=models.PROTECT)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"


class Order(models.Model):
    STATUS_NEW = "new"
    STATUS_CONFIRMED = "confirmed"
    STATUS_DELIVERING = "delivering"
    STATUS_DONE = "done"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_DELIVERING, "Delivering"),
        (STATUS_DONE, "Done"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="orders")
    restaurant = models.ForeignKey("catalog.Restaurant", on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    delivery_fee = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.pk} — {self.user} — {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    menu_item = models.ForeignKey("catalog.MenuItem", on_delete=models.PROTECT)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.quantity}x {self.item_name}"


class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="options")
    option_name = models.CharField(max_length=120)
    price_delta = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.option_name} (+{self.price_delta})"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class OrderPromo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="promos")
    promo = models.ForeignKey(PromoCode, on_delete=models.PROTECT)
    applied_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.promo.code} on order {self.order_id}"


class Payment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_SUCCEEDED = "succeeded"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_SUCCEEDED, "Succeeded"),
        (STATUS_FAILED, "Failed"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    provider = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} {self.amount} — {self.status}"
