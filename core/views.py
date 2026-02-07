from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Customer

def shop_view(request):
    # 1. Fetch Products for the "Daily Discover" section
    products = Product.objects.all()
    
    # 2. CART LOGIC: Fetch the current 'pending' order
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

def home(request):
    # Fetch all products
    products = Product.objects.all()
    
    # Render the new 'home.html' template
    return render(request, 'core/home.html', {'products': products})


def add_to_cart(request, product_id):
    # 1. Get the specific product user wants to buy
    product = get_object_or_404(Product, id=product_id)

    # 2. Get the "dummy" customer (For now, we just grab the first one in the DB)
    """# NOTE: You MUST have created at least one Customer in Admin Panel for this to work! """
    customer = Customer.objects.first() 

    # 3. Get or Create a Pending Order for this customer
    # (If they have a pending order, use it. If not, make a new one.)
    order, created = Order.objects.get_or_create(
        customer=customer, 
        order_status='pending'
    )

    # 4. Check if this product is already in the cart
    item, created = OrderItem.objects.get_or_create(
        order=order, 
        product=product,
        defaults={'quantity': 0, 'price_at_purchase': product.price}
    )

    # 5. Increase Quantity and Save
    item.quantity += 1
    item.save()

    # 6. Redirect the user to the Cart page to see their item
    return redirect('cart')