from django.shortcuts import render,redirect,get_object_or_404
from .forms import AdminLoginForms,AddCategoryForms
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages,auth
from django.http import HttpResponse
from orders.models import Order,Payment,OrderProduct
from category.models import Category
from store.models import Product
from django.db.models import Sum
from django.utils import timezone
from django.forms.models import model_to_dict

# Create your views here.
def login(request):
    if request.method == 'POST':
        admin_login = AdminLoginForms(request.POST)
        if admin_login.is_valid():
            username = admin_login.cleaned_data.get('username')
            password = admin_login.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password, superadmin=True)
            if user is not None:
                auth_login(request,user)
                return redirect('admin_dashboard')
            else:
                messages.error(request,'รหัสผ่านไม่ถูกต้อง')
                return redirect('backoffice_login')

    else:
        admin_login = AdminLoginForms()
        context = {
            "admin_login":admin_login
        }
        return render(request, 'backoffice/login.html',context)

def logout(request):
    auth.logout(request)
    messages.success(request, 'คุณออกจากระบบเรียบร้อยแล้ว')
    return redirect('backoffice_login')

def order_detail(request,order_number):
    orders = Order.objects.get(order_number=order_number)
    order_products = OrderProduct.objects.filter(order_id=orders.id)

    context = {
        'orders': orders,
        'order_products' : order_products
    }

    return render(request, 'backoffice/order_detail.html', context)


def add_product(request):
    product = Product.objects.filter().order_by('-created_date')
    categories = Category.objects.filter()
    product_add = Product()
    category_add_form = AddCategoryForms()

    if request.method == 'POST':
        product_add.product_name = request.POST['product_name']
        product_add.slug = request.POST['slug'].replace(' ','-')
        product_add.description = request.POST['description']
        product_add.price = request.POST['price']
        product_add.stock = request.POST['stock']
        product_add.is_available = 'available' in request.POST

        image = request.FILES.get('product_image', None)
        if image:
            product_add.images = image 

        category_name = request.POST['category']
        category = Category.objects.get(category_name=category_name)
        product_add.category = category


        product_add.save()
        messages.success(request,'เพิ่มสินค้าสำเร็จ')
        return redirect('add_product')
    else:
        messages.error(request,'เพิ่มสินค้าไม่สำเร็จกรุณากรอกข้อมูลให้ครบถ้วน')
        
    

    context = {
        'product': product,
        'categories':categories,
        'category_add_form':category_add_form
    }
    return render(request, 'backoffice/add_product.html',context)

def edit_product(request, choices, product_id):
    product = Product.objects.get(id=product_id)

    if choices == 'delete':
        product.delete()
        
    elif choices == 'edit':
        if request.method == 'POST':
            product.product_name = request.POST['product_name']
            product.slug = request.POST['slug'].replace(' ','-')
            product.description = request.POST['description']
            product.price = request.POST['price']
            product.stock = request.POST['stock']
            product.is_available = 'available' in request.POST

            image = request.FILES.get('product_image', None)
            if image:
                product.images = image

            category_name = request.POST['category']
            category = Category.objects.get(category_name=category_name)
            product.category = category

            product.save()

    return redirect('add_product')

def edit_category(request,edit,category_id):
    category = Category.objects.get(id=category_id)
    if edit == 'delete':
        category.delete()
    return redirect('add_product')

def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForms(request.POST)
        if form.is_valid:
           form.save()
           messages.success(request,('เพิ่มหมวดหมู่สำเร็จ'))
         
        else:
            messages.error(request,('เพิ่มหมวดหมู่ไม่สำเร็จ'))

    return redirect('add_product')

def update_payment_status(request,status,payment_id,order_id):
    payment = Payment.objects.get(id=payment_id) # Payment
    order = Order.objects.get(id=order_id)

    if status == 'Approve':
        payment.status = 'Approved'
        payment.save()
    elif status == 'Reject':
        payment.status = 'Rejected'
        payment.save()
        order.order_status = 'Cancelled'
        order.save()
    else:
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')

def update_order_status(request,status,order_id):
    order = Order.objects.get(id=order_id)

    if status == 'Completed':
        order.order_status = 'Completed'
        order.save()
        messages.success(request,'เปลี่ยนสถานะเป็นส่งพัสดุสำเร็จ')
    elif status == 'Cancelled':
        order.order_status = 'Cancelled'
        order.save()
        messages.error(request,'ยกเลิกสินค้าแล้ว')
    else:
        return redirect('admin_dashboard')

    
    return redirect('admin_dashboard')

def admin_dashboard(request):
    orders = Order.objects.filter().order_by("-created_at") #แสดงออร์เดอร์ทั้งหมด และเรียงลำดับจากมากไปน้อย
    bills = Payment.objects.filter().order_by("-created_at") #แสดงใบเสร็จที่มีการชำระเงินแล้วทั้งหมด และเรียงลำดับจากมากไปน้อย
    sum_order = Order.objects.filter(order_status='Accepted').count() # [Order, Order, Order, Order]
    pending_payments_count = Payment.objects.filter(status='Pending').count()

    today = timezone.now().date()

    today_total_income = Payment.objects.filter(
        status='Approved',
        updated_at__gte=today
    ).aggregate(total=Sum('amount_paid'))['total'] or 0





    context={
        'orders': orders,
        'bills': bills,
        'sum_order':sum_order,
        'today_total_income': today_total_income,
        'pending_payments_count': pending_payments_count,
    }
    return render(request, 'backoffice/admin_dashboard.html',context)

