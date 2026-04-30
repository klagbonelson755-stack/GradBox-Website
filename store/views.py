from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Package, Order, OrderItem


def home(request):
    """Home page with package categories"""
    packages = Package.objects.filter(is_active=True)

    # Group packages by category
    categories = {
        'facials': packages.filter(category='facials'),
        'foodstuffs': packages.filter(category='foodstuffs'),
        'phone': packages.filter(category='phone'),
        'breakfast': packages.filter(category='breakfast'),
    }

    # Get cart count
    cart = request.session.get('cart', {})
    cart_count = len(cart)

    context = {
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'store/home.html', context)


def packages(request):
    """All packages page"""
    packages = Package.objects.filter(is_active=True)
    category_filter = request.GET.get('category')

    if category_filter:
        packages = packages.filter(category=category_filter)

    # Get cart
    cart = request.session.get('cart', {})
    cart_count = len(cart)

    context = {
        'packages': packages,
        'category_filter': category_filter,
        'cart_count': cart_count,
    }
    return render(request, 'store/packages.html', context)


def package_detail(request, package_id):
    """Single package detail view"""
    package = get_object_or_404(Package, id=package_id, is_active=True)

    # Get cart count
    cart = request.session.get('cart', {})
    cart_count = len(cart)

    # Check if in cart
    in_cart = str(package_id) in cart

    context = {
        'package': package,
        'cart_count': cart_count,
        'in_cart': in_cart,
    }
    return render(request, 'store/package_detail.html', context)


@login_required
def add_to_cart(request, package_id):
    """Add package to cart"""
    package = get_object_or_404(Package, id=package_id, is_active=True)

    cart = request.session.get('cart', {})

    # Add package to cart (using package ID as key)
    if str(package_id) not in cart:
        cart[str(package_id)] = {
            'package_id': package.id,
            'name': package.name,
            'price': str(package.price),
            'student_price': str(package.get_student_price()),
            'category': package.category,
            'image_url': package.image_url,
        }
        request.session['cart'] = cart
        messages.success(request, f'{package.name} added to cart!')
    else:
        messages.info(request, f'{package.name} is already in your cart!')

    return redirect('cart')


@login_required
def remove_from_cart(request, package_id):
    """Remove package from cart"""
    cart = request.session.get('cart', {})

    if str(package_id) in cart:
        del cart[str(package_id)]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart!')

    return redirect('cart')


@login_required
def cart(request):
    """Shopping cart view"""
    cart = request.session.get('cart', {})
    cart_items = list(cart.values())

    # Check if user is verified student for discount
    is_student = False
    if hasattr(request.user, 'profile'):
        is_student = request.user.profile.is_student and request.user.profile.is_verified

    # Calculate totals
    subtotal = 0
    for item in cart_items:
        if is_student:
            subtotal += float(item['student_price'])
        else:
            subtotal += float(item['price'])

    context = {
        'cart_items': cart_items,
        'cart_count': len(cart),
        'subtotal': subtotal,
        'is_student': is_student,
    }
    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):
    """Checkout view"""
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('packages')

    cart_items = list(cart.values())

    # Check student discount
    is_student = False
    if hasattr(request.user, 'profile'):
        is_student = request.user.profile.is_student and request.user.profile.is_verified

    # Calculate total
    total = 0
    for item in cart_items:
        if is_student:
            total += float(item['student_price'])
        else:
            total += float(item['price'])

    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            delivery_location=request.POST.get('delivery_location'),
            contact_phone=request.POST.get('contact_phone'),
            payment_method=request.POST.get('payment_method'),
            student_discount_applied=is_student,
            total_amount=total,
        )

        # Create order items
        for item in cart_items:
            package = Package.objects.get(id=item['package_id'])
            price = float(item['student_price']
                          ) if is_student else float(item['price'])
            OrderItem.objects.create(
                order=order,
                package=package,
                quantity=1,
                price_at_purchase=price,
            )

        # Clear cart
        request.session['cart'] = {}

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_confirmation', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total': total,
        'is_student': is_student,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.order_items.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_confirmation.html', context)


@login_required
def my_orders(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'store/my_orders.html', context)
