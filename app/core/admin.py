from django.contrib import admin
from .models import User, InviteCode, Category, Product, Card, Order, ApiLog
admin.site.register([User, InviteCode, Category, Product, Card, Order, ApiLog])
