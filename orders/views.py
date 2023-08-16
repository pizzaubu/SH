from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm,PaymentForm
import datetime
from .models import Account, Order, Payment, OrderProduct
import json
from store.models import Product, Coupon
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def payments(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        amount_paid = float(request.POST.get('amount_paid'))
        status = request.POST.get('status')
        form = PaymentForm(request.POST, request.FILES)
        

        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            images = form.cleaned_data['images']
            user = request.user
            payment = None
            
            # Get the order with is_ordered=False for the current user
            order = Order.objects.filter(user=request.user, is_ordered=False).order_by("-created_at").first()
            if order: # if order is not None
                payment = Payment(
                    user=user,
                    payment_id=f'{email}-{payment_method}-{amount_paid}',
                    payment_method=payment_method,
                    amount_paid=amount_paid,
                    status=status,
                    images=images
                )
                payment.save()
                order_number = order.order_number
                order.payment = payment
                order.is_ordered = True
                order.order_status = 'Accepted'
                order.save()

            else:
                return redirect('home')

            Order.objects.filter(user=request.user, is_ordered=False).update(is_ordered=True, order_status = 'Cancelled')

            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                #บันทึกประวัติการสั่งซื้อลง OrderProduct
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.payment = payment
                order_product.user = user
                order_product.product = item.product
                order_product.quantity = item.quantity
                order_product.product_price = item.product.price
                order_product.save()

                # ลดจำนวนสินค้าที่วางขาย
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()

            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_price * i.quantity

            order_discount = 0
            if order.coupon is not None:
                order_discount += (subtotal + order.shipping) * (order.coupon.discount/100)



            # ลบสินค้าในตะกร้าหลังจากทำการชำระเงินเสร็จสิ้น
            CartItem.objects.filter(user=request.user).delete()

            context = {
                'order':order,
                'payment':payment,
                'ordered_products':ordered_products,
                'order_number':order_number,
                'subtotal':subtotal,
                'order_discount':order_discount

            }

            return render(request, 'orders/order_complete.html',context)

@login_required(login_url='login')
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    order_form = OrderForm(request.POST)
    payment_form = PaymentForm(request.POST)
    total = float(request.POST.get("total"))
    shipping = float(request.POST.get("shipping"))
    grand_total = total + shipping
    coupon_code = request.POST.get("coupon") # 123ABC
    coupon = None
    discount = 0
    
    if coupon_code != "None":
        coupon = Coupon.objects.get(code=coupon_code) # type coupon object
        discount = grand_total * (coupon.discount/100)
        
    final_prize = grand_total - discount

    if request.method == 'POST':
        if order_form.is_valid():
             # จัดเก็บข้อมูลที่อยู่สำหรับการเรียกเก็บเงินภายในตาราง Order
            data = Order()
            data.user = current_user
            data.first_name = order_form.cleaned_data['first_name']
            data.last_name = order_form.cleaned_data['last_name']
            data.phone = order_form.cleaned_data['phone']
            data.email = order_form.cleaned_data['email']
            data.address_line_1 = order_form.cleaned_data['address_line_1']
            data.address_line_2 = order_form.cleaned_data['address_line_2']
            data.state = order_form.cleaned_data['state']
            data.order_note = order_form.cleaned_data['order_note']
            data.order_total = total
            data.shipping = shipping
            data.coupon = coupon
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # สร้างหมายเลขคำสั่งซื้อ
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20230305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'shipping': shipping,
                'coupon':coupon,
                'discount':discount,
                'final_prize': final_prize,
                'order_form': order_form,
                'payment_form':payment_form
                
            }
            return render(request, 'orders/payments.html', context)
    else:
        order_form = OrderForm()
        context = {
            'order_form': order_form
        }
        return redirect('checkout')

@login_required
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store')    

@login_required
def order_detail(request, order_number):
    
    order = Order.objects.get(order_number=order_number)
    order_product = OrderProduct.objects.filter(order_id=order.id) # []

    print(order.id)
    print(order_product)

    context = {
        'order': order, # Order
        'order_product': order_product # [OrderProduct, ]
    }

    return render(request, 'orders/order_detail.html', context)




    


