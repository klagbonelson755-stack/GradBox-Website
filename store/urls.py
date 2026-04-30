from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('add-to-cart/<int:package_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:package_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_confirmation,
         name='order_confirmation'),
    path('orders/', views.my_orders, name='my_orders'),
]
