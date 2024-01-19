from django.urls import path

from . import views

urlpatterns = [
    path("ping", views.ping, name="ping"),
    path("trade", views.trade, name="trade"),
    path("account", views.account, name="account"),
]
