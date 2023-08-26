from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating,Coupon
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from django.utils import timezone
from carts.views import _cart_id
from django.core.paginator import Paginator
from .forms import ReviewForm
from orders.models import OrderProduct
from django.http import JsonResponse




def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True) # list

    sum_rating = 0
    rating_avg = 0
    yellow_star_avg = range(0)
    grey_star_avg = range(0)
    yellow_half_avg = False
    
    if len(reviews) >= 1 :
        for i in range(len(reviews)):
            reviews[i].yellow_star = range(int(reviews[i].rating))
            reviews[i].grey_star = range(5-int(reviews[i].rating))
            reviews[i].format_created_at = reviews[0].created_at.strftime("%d/%m/%Y %H:%M")
            sum_rating  += reviews[i].rating
     
    
        rating_avg = sum_rating/len(reviews)# type float # 3.3333333
        yellow_star_avg = range(int(rating_avg)) # range(0,3)
        grey_star_avg = range(5-int(rating_avg)) # range(0,2)

        if(rating_avg-int(rating_avg) >= 0.5): # 3.3333333 - 3 = 0.33333
            yellow_half_avg = True
            grey_star_avg = range(5-1-int(rating_avg)) # range(0,1)
        
    review_form = ReviewForm()

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct'  : orderproduct,
        'reviews'       : reviews,
        'products_by_category' : single_product.category.category_name, # Add this line to include the category name
        'stock_range'   : range(1, single_product.stock + 1),
        'rating_avg' : f"{rating_avg:.2f}", # 3.333333
        'yellow_half_avg' : yellow_half_avg,
        'yellow_star_avg' : yellow_star_avg,
        'grey_star_avg' : grey_star_avg,
        'review_form': review_form
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print("user =>",request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = request.POST['product_id']
            review.ip = request.META.get('REMOTE_ADDR')
            review.save()
            return redirect('product_detail', category_slug=review.product.category.slug, product_slug=review.product.slug)
    return redirect('store')


def get_coupon(code):
    try:
        coupon = Coupon.objects.get(code=code)

        if coupon.is_active and (coupon.valid_from <= timezone.now()) and (coupon.valid_to >= timezone.now()):
            return coupon
        else:
            return None
    except Coupon.DoesNotExist:
        return None
    

def apply_coupon(request):
    code = request.GET.get('code', '')
    coupon = get_coupon(code)

    if coupon:
        data = {
            'success': True,
            'code': coupon.code,
            'discount': coupon.discount,
        }
    else:
        data = {
            'success': False,
            'message': 'Invalid coupon code or the coupon is expired.',
        }

    return JsonResponse(data)

    
def product_filter(request):
    # ตัวอย่างของการสร้างลิสต์หมวดหมู่
    categories = Category.objects.all()
    
    # รับค่าหมวดหมู่ที่เลือก
    selected_category = request.GET.get('category', None)

        # รับค่าตัวกรองราคาจากคำขอ
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    selected_category = request.GET.get('category', None)

    # กรองสินค้าตามหมวดหมู่ที่เลือก (ถ้ามีการระบุ)
    products = Product.objects.all()
    if selected_category is not None and selected_category != '':
        try:
            selected_category = int(selected_category)
            products = products.filter(category__id=selected_category)
        except ValueError:
            pass  # ใช้ค่าเริ่มต้นที่คือสินค้าทั้งหมด

    # กรองรายการสินค้าตามช่วงราคาที่ระบุ
    if min_price is not None and max_price is not None and min_price != '' and max_price != '':
        try:
            min_price = int(min_price)
            max_price = int(max_price)
            products = products.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass  # ใช้ค่าเริ่มต้นที่คือสินค้าทั้งหมด

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'store/store.html', context)

