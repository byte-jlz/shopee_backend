from django.db import models

# 1. Customer Table
class Customer(models.Model):
    # 'id' is created automatically as the Primary Key (PK)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.username

# 2. UserAddress Table
class UserAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient_name} - {self.city}"

# 3. Shop Table
class Shop(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_description = models.TextField()
    shop_rating = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.shop_name

# 4. Category Table
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

# 5. Product Table
class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.product_name

# 6. Orders Table
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id}"

# 7. OrderItem Table (The Bridge)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

# 8. Payment Table
class Payment(models.Model):
    PAYMENT_METHODS = [('cod', 'COD'), ('gcash', 'GCash')]
    PAYMENT_STATUS = [('paid', 'Paid'), ('pending', 'Pending')]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"