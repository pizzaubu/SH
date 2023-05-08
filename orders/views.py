from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm,ReturnForm
import datetime
from .models import Account, Order, Payment, OrderProduct
import json
from store.models import Product, Coupon
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def payments(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        payment_method = request.POST.get('payment_method')
        amount_paid = request.POST.get('amount_paid')
        status = request.POST.get('status')
        images = request.FILES.get('images')  # Get the uploaded image file

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'User not found'})

        payment = Payment(
            user=user,
            payment_id=f'{email}-{payment_method}-{amount_paid}',
            payment_method=payment_method,
            amount_paid=amount_paid,
            status=status,
            images=images
        )
        payment.save()

        response_data = {
            'payment_id': payment.payment_id,
            'user_id': email,
            'payment_method': payment.payment_method,
            'amount_paid': payment.amount_paid,
            'status': payment.status,
            'created_at': payment.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'images': payment.images.url  # Add the image URL to the response data
        }

        # ลบสินค้าในตะกร้าหลังจากทำการชำระเงินเสร็จสิ้น
        CartItem.objects.filter(user=request.user).delete()

        return JsonResponse(response_data)

    return render(request, 'orders/order_complete.html')



@login_required(login_url='login')
def place_order(request):
    current_user = request.user

    # หากจำนวนสินค้าในตะกร้าน้อยกว่าหรือเท่ากับ 0 ให้กลับไปที่หน้าร้านค้า
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    order_form = OrderForm(request.POST)
    total = float(request.POST.get("total"))
    tax = float(request.POST.get("tax"))
    coupon_code = request.POST.get("coupon") # 123ABC
    coupon = None
    discount = 0
    
    if coupon_code != "None":
        coupon = Coupon.objects.get(code=coupon_code) # type coupon object
        discount = total * (coupon.discount/100)
        
    final_prize = total + tax - discount

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
            data.tax = tax
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
                'tax': tax,
                'coupon':coupon,
                'discount':discount,
                'final_prize': final_prize,
                'order_form': order_form
                
            }
            return render(request, 'orders/payments.html', context)
    else:
        order_form = OrderForm()
        context = {
            'order_form': order_form
        }
        return redirect('checkout')
    
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
        return redirect('home')

def refund(request):
    if request.method == 'POST':
        return_form = ReturnForm(request.POST)
        if return_form.is_valid():
            refund_request = return_form.save(commit=False)
            refund_request.email = request.user.email
            refund_request.save()
            return redirect('success_page')
    else:
        return_form = ReturnForm()

    # สร้าง dictionary เพื่อส่งตัวแปร context ไปยัง template
    context = {
        'return_form': return_form,
        'title': 'Request Refund',  # ตัวอย่างสร้าง title
    }
    return render(request, 'orders/refund.html', context)
