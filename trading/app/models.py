from django.db import models

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=50)
    order_direction = models.CharField(max_length=5)
    order_date_open = models.DateTimeField("date published")
    order_date_close = models.DateTimeField("date published")
    order_amount_open = models.DecimalField(max_digits=10, decimal_places=8)
    order_amount = models.DecimalField(max_digits=10, decimal_places=8)


class Position(models.Model):
    position_id = models.CharField(max_length=50)
    position_direction = models.CharField(max_length=5)
    position_date_open = models.DateTimeField("date published")
    position_date_close = models.DateTimeField("date published")
    position_amount_open = models.DecimalField(max_digits=10, decimal_places=8)
    position_amount_close = models.DecimalField(max_digits=10, decimal_places=8)
    position_profit_loss = models.DecimalField(max_digits=10, decimal_places=8)
    position_win = models.BooleanField()
