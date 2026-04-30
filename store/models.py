from django.db import models
from django.contrib.auth.models import User


class Package(models.Model):
    """Product packages available for purchase"""

    CATEGORY_CHOICES = [
        ('facials', 'Facials'),
        ('foodstuffs', 'Foodstuffs'),
        ('phone', 'Phone & Accessories'),
        ('breakfast', 'Breakfast'),
    ]

    name = models.CharField(max_length=200, verbose_name='Package Name')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, verbose_name='Category')
    description = models.TextField(verbose_name='Description')
    items = models.JSONField(verbose_name='Items Included')
    image_url = models.URLField(verbose_name='Product Image URL')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Regular Price (GH₵)')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Package'
        verbose_name_plural = 'Product Packages'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    def get_student_price(self):
        """Calculate 40% discounted price for students"""
        discount = self.price * 0.40
        return self.price - discount


class Order(models.Model):
    """Customer orders"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    packages = models.ManyToManyField(
        Package, through='OrderItem', related_name='orders')
    delivery_location = models.CharField(
        max_length=300, verbose_name='Delivery Location')
    contact_phone = models.CharField(
        max_length=20, verbose_name='Contact Phone')
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, verbose_name='Payment Method')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    student_discount_applied = models.BooleanField(default=False)
    notes = models.TextField(blank=True, verbose_name='Order Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def calculate_total(self):
        """Calculate total based on student discount"""
        total = 0
        for item in self.order_items.all():
            if self.student_discount_applied:
                total += item.package.get_student_price() * item.quantity
            else:
                total += item.package.price * item.quantity
        self.total_amount = total
        return total


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.package.name} x {self.quantity}"

    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.price_at_purchase * self.quantity
