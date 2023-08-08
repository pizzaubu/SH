from datetime import timezone
from django.shortcuts import render
from django.forms.models import model_to_dict

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from store.models import Coupon
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm


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
@login_required(login_url='login')
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
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user, quantity=0, is_active=True, cart=cart)

    # รับค่าจำนวนสินค้าที่ผู้ใช้เลือก
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    cart_item.quantity += quantity
    cart_item.save()

    return redirect('cart')


@login_required(login_url='login')
def update_cart(request, cart_id, product_id,action):
    
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, cart_id=cart_id)
    cart_item_update = CartItem.objects.get(product=product, cart=cart)
    if action == 'increment':
        cart_item_update.quantity += 1
    else:
        cart_item_update.quantity -= 1
    cart_item_update.save()
    return redirect('cart')

def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, is_active=True)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    cart_items = _get_cart_items(request)
    total, quantity = _calculate_cart_total(cart_items)
    tax, grand_total = _calculate_tax_and_grand_total(total)
    
    coupon_code = request.GET.get("coupon") # 123abc
    order_form = OrderForm(initial=model_to_dict(request.user))
    #print(coupon_code)
    # coupon code is not empty
    coupon = None
    discount = 0
    final_prize = grand_total
    if(coupon_code):
        coupon = Coupon().get_coupon(coupon_code) # call function
        if coupon is not None :
            discount = grand_total * (coupon.discount/100) # 34680 * 10
            final_prize = grand_total - discount

        
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'coupon': coupon,
        'discount': discount,
        'final_prize': final_prize,
        'order_form': order_form
    }
    return render(request, 'store/checkout.html', context)


