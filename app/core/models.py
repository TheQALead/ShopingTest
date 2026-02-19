import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('STUDENT', 'STUDENT'), ('VIZOR', 'VIZOR'), ('ADMIN', 'ADMIN'))
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    is_email_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class InviteCode(models.Model):
    code = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_uses = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)

class Category(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    visible = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    masked_pan = models.CharField(max_length=24)
    brand = models.CharField(max_length=20, default='UNKNOWN')
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    card_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_default = models.BooleanField(default=False)

class Order(models.Model):
    STATUS = (
        ('CREATED', 'CREATED'), ('PAID_SIMULATED', 'PAID_SIMULATED'),
        ('PAID_3DS_REQUIRED', 'PAID_3DS_REQUIRED'), ('SHIPPED_SIMULATED', 'SHIPPED_SIMULATED'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default='CREATED')
    total = models.DecimalField(max_digits=10, decimal_places=4, default=0)

class ApiLog(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    status = models.IntegerField()
    latency_ms = models.IntegerField()
    request_headers = models.JSONField(default=dict)
    request_body = models.TextField(blank=True)
    response_body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
