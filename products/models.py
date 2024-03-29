from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


from shared.models import BaseModel

from shared.uitility import phone_regex
from users.models import User

OrderProcessing, Shipped, ReadyToPickUup, Canceled, Delivered, Empty = (
'OrderProcessing', 'shipped', 'readyToPickUup', 'cancelled', 'Delivered', 'Empty'
)
class Product(BaseModel):
    PRODUCT_STATUS = (
        ('OrderProcessing', 'Order Processing'),
        ('ReadyToPickUp', 'Ready to Pick Up'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Empty', 'Empty')
    )
    product_status = models.CharField(max_length=31, choices=PRODUCT_STATUS, default='Empty')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    month_price = models.PositiveIntegerField(default=0, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    image = models.FileField(upload_to='products/images/', null=True, blank=True)
    slug = models.SlugField(default='', null=True, unique=True)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True
    )

    likes = models.IntegerField(default=0, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    discount_title = models.TextField(null=True, blank=True)
    discount_start_time = models.DateTimeField(null=True, blank=True)
    discount_end_time = models.DateTimeField(null=True, blank=True)

    def is_discount_active(self):
        now = timezone.now()
        return self.discount_start_time and self.discount_end_time and self.discount_start_time <= now <= self.discount_end_time

    @property
    def new_price(self):
        if self.discount:
            discount_percentage = self.discount / 100
            new_price = self.price - (discount_percentage * self.price)
            return new_price
        return None

    def __str__(self):
        return f"{self.title} {self.price}"


class Category(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
       return f"Category name ->  {self.name}"

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" comment-> {self.product.title} by {self.user}"


class Cart(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='cart')
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return f" cart-> {self.product.title} by {self.user} qty -> {str(self.quantity)}"


class Order(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='order')
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    active_phone_number = models.CharField(max_length=31, unique=True, validators=[phone_regex])
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} by {self.user.username} quantity -> {self.quantity}"