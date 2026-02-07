from django.urls import path
from . import views

urlpatterns = [
    # This says: "When user visits the homepage (''), call the shop_view function"
    path('', views.home, name='home'),

    path('cart/', views.shop_view, name='cart'),

    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('plus/<int:product_id>/', views.plus_cart_item, name='plus_cart'),
    path('minus/<int:product_id>/', views.minus_cart_item, name='minus_cart'),
    path('remove/<int:product_id>/', views.remove_cart_item, name='remove_cart'),

]