from django.db import models
from django.core.validators import MinValueValidator


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu_items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cuisines = models.ManyToManyField(
        Cuisine,
        blank=True,
        related_name="menu_items"
    )
    categories = models.ManyToManyField(
        "Category",
        through="ItemCategory",
        related_name="menu_items"
    )

    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"


class ItemCategory(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)

    class Meta:
        unique_together = ("item", "category")
        ordering = ["position"]

    def __str__(self):
        return f"{self.item.name} in {self.category.name}"


class Option(models.Model):
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ItemOption(models.Model):
    item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="item_options"
    )
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ("item", "option")

    def __str__(self):
        return f"{self.option.name} for {self.item.name}"


class DeliveryZone(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="delivery_zones"
    )
    name = models.CharField(max_length=120)
    min_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    fee = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"
