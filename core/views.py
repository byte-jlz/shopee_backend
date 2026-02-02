from django.shortcuts import render
from .models import Product, Order, OrderItem

def shop_view(request):
    # 1. Fetch Products for the "Daily Discover" section
    products = Product.objects.all()
    
    # 2. CART LOGIC: Fetch the current 'pending' order
    # Note: In a real app with login, you would filter by the logged-in user (e.g., customer=request.user.customer)
    # For now, we get the *last* pending order created in the system to test.
    cart_order = Order.objects.filter(order_status='pending').last()

    cart_items = []
    cart_total = 0

    if cart_order:
        # Get all items inside this specific order
        cart_items = OrderItem.objects.filter(order=cart_order)
        
        # Calculate Total: Loop through items and add (price * quantity)
        for item in cart_items:
            cart_total += item.price_at_purchase * item.quantity

    # 3. CONTEXT: Send everything to the HTML
    context = {
        'products': products,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'shop.html', context)