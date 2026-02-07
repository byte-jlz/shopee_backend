from django.urls import path
from . import views

urlpatterns = [
    # This says: "When user visits the homepage (''), call the shop_view function"
    path('', views.home, name='home'),

    path('cart/', views.shop_view, name='cart'),

    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

]