from django.urls import path
from . import views

urlpatterns = [
    # This says: "When user visits the homepage (''), call the shop_view function"
    path('', views.shop_view, name='shop'),
]