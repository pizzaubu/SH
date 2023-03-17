from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def _get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        return CartItem.objects.filter(cart=cart, is_active=True)

def _calculate_cart_total(cart_items):
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    return total, quantity

def _calculate_tax_and_grand_total(total):
    tax = (2 * total) / 100
    grand_total = total + tax
    return tax, grand_total


# ... (เก็บโค้ดฟังก์ชัน add_cart, remove_cart, remove_cart_item ไว้ที่นี่) ...

def cart(request):
    cart_items = _get_cart_items(request)
    total, quantity = _calculate_cart_total(cart_items)
    tax, grand_total = _calculate_tax_and_grand_total(total)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request):
    cart_items = _get_cart_items(request)
    total, quantity = _calculate_cart_total(cart_items)
    tax, grand_total = _calculate_tax_and_grand_total(total)

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
