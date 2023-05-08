from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('coupon/<str:code>/', views.coupon_detail, name='coupon_detail'),
    path('get_coupon/', views.get_coupon, name='get_coupon'),
    path('product_filter/',views.product_filter,name='product_filter'),


]
