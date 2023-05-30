from django.shortcuts import render, redirect
from .forms import RegistrationForm,LoginForm,ProfilePictureForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests
from django.contrib.auth import authenticate, login
from orders.forms import OrderForm
from orders.models import Order

def generate_unique_username(username_base):
    username = username_base
    counter = 1

    while User.objects.filter(username=username).exists():
        username = f"{username_base}{counter}"
        counter += 1

    return username

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'] # test2
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password,address=address)
            user.phone_number = phone_number
            user.is_active = True  # ให้ user นี้เปิดใช้งาน
            user.save()

        # การเปิดใช้งานผู้ใช้
        """current_site = get_current_site(request)
        mail_subject = 'กรุณายืนยันการเปิดใช้งานบัญชีของคุณ'
        message = render_to_string('accounts/account_verification_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()"""
        # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
        #return redirect('/accounts/login/?command=verification&email='+email)
        messages.success(request, 'ลงทะเบียนสำเร็จกรุณาล๊อคอิน')
        return redirect('login')
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)

            



def do_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else: 
            return redirect("login")
    else:
        login_forms = LoginForm()
        context = {
            'login_forms': login_forms
        }
        return render(request, 'accounts/login.html',context)


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'คุณออกจากระบบเรียบร้อยแล้ว')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'ยินดีด้วย! บัญชีของคุณได้รับการเปิดใช้งานแล้ว')
        return redirect('login')
    else:
        messages.error(request, 'ลิงค์เปิดใช้งานไม่ถูกต้อง')
        return redirect('register')


@login_required
def dashboard(request):
    # ดึงข้อมูลการสั่งซื้อทั้งหมดของผู้ใช้
    orders = Order.objects.filter(user=request.user)
    order = orders.latest('created_at') if orders.exists() else None

    # สร้าง instance ของ ProfilePictureForm
    form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=request.user)

    # ตรวจสอบการส่งข้อมูล POST
    if request.method == 'POST':
        if form.is_valid():
            # บันทึกข้อมูลที่ได้จากฟอร์ม
            form.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'There was an error updating your profile picture.')

    context = {
        'order': order,
        'orders':orders,
        'form': form,  # ส่ง form instance ไปที่ template
    }

    return render(request, 'accounts/dashboard.html', context)




def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'ตั้งค่ารหัสผ่านใหม่ของคุณ'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'อีเมล์ตั้งค่ารหัสผ่านใหม่ถูกส่งไปยังที่อยู่อีเมล์ของคุณแล้ว')
            return redirect('login')
        else:
            messages.error(request, 'ไม่พบบัญชี!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'กรุณาตั้งค่ารหัสผ่านใหม่ของคุณ')
        return redirect('resetPassword')
    else:
        messages.error(request, 'ลิงก์นี้หมดอายุแล้ว!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'การตั้งค่ารหัสผ่านเสร็จสมบูรณ์')
            return redirect('login')
        else:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
