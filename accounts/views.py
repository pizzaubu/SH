from django.shortcuts import render, redirect
from .forms import RegistrationForm,LoginForm,ProfilePictureForm,ProfileSettingForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from orders.models import Order
from django.forms.models import model_to_dict

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'] # test2
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.is_active = True  # ให้ user นี้เปิดใช้งาน
            user.save()

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
            messages.error(request,'รหัสผ่านไม่ถูกต้อง') 
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


@login_required
def dashboard(request):
    # ดึงข้อมูลการสั่งซื้อทั้งหมดของผู้ใช้
    orders = Order.objects.filter(user=request.user) # [Order, Order, Order]
    order = orders.latest('created_at') if orders.exists() else None # Order

   
    context = {
        'order': order,
        'orders':orders,
          
    }

    return render(request, 'accounts/dashboard.html', context)



@login_required
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = Account.objects.get(username=request.user.username)
            user.set_password(password)
            user.save()
            messages.success(request, 'การตั้งค่ารหัสผ่านเสร็จสมบูรณ์')
            return redirect('login')
        else:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

def setting(request):
    picture_form = ProfilePictureForm()
    if request.method == 'POST':
        profile_edit_form = ProfileSettingForm(request.POST, instance=request.user)
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            messages.success(request, 'Profile editing successful!')
        else:
            messages.error(request, 'There was an error from editing your profile.')

        profilepicture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if profilepicture_form.is_valid():
            # บันทึกข้อมูลที่ได้จากฟอร์ม
            profilepicture_form.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'There was an error updating your profile picture.')
      

    # สร้าง form ใหม่กับข้อมูลที่อัพเดทแล้ว
    setting_form = ProfileSettingForm(initial=model_to_dict(request.user))

    context = {
        'setting_form': setting_form,
        'picture_form': picture_form
    }

    return render(request, 'accounts/profile_setting.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']  # ข้อมูล email ที่รับเข้ามา
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        try:
            user = Account.objects.get(email=email)  # ลองดึง user จาก database ด้วย email
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'การตั้งค่ารหัสผ่านเสร็จสมบูรณ์')
                return redirect('login')
            else:
                messages.error(request, 'รหัสผ่านไม่ตรงกัน!')
                return redirect('resetPassword')
        except Account.DoesNotExist:
            messages.error(request, 'ไม่พบ email กรุณากรอก email ที่ถูกต้อง หรือสมัครสมาชิกใหม่')
            return redirect('forgot_password')
    else:
        return render(request, 'accounts/forgot_password.html')