from django.contrib import admin

# Register your models here.
from app.models import Order, Position

admin.site.register(Order)
admin.site.register(Position)
