from django.contrib import admin
from .models import Package, Order, OrderItem


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

    fieldsets = (
        ('Package Information', {
            'fields': ('name', 'category', 'description', 'items', 'image_url', 'price', 'is_active')
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['package', 'quantity', 'price_at_purchase']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount',
                    'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'student_discount_applied']
    search_fields = ['user__username', 'id', 'delivery_location']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'total_amount', 'delivery_location', 'contact_phone',
                       'payment_method', 'student_discount_applied', 'created_at', 'updated_at']
