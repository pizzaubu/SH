from django.contrib import admin
from .models import Product, ReviewRating, Coupon

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

    # เพิ่มความสามารถในการกรองข้อมูล
    list_filter = ('category', 'is_available')

    # เพิ่มความสามารถในการค้นหาข้อมูล
    search_fields = ('product_name', 'category__category_name')

    # เพิ่มความสามารถในการเรียงลำดับข้อมูล
    list_per_page = 20
    ordering = ('-modified_date',)

# สำหรับ CouponAdmin เราจะใช้ list_display เพื่อเลือกแสดงข้อมูลที่ต้องการในรายการ
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'is_active')

    # เพิ่มความสามารถในการกรองข้อมูล
    list_filter = ('is_active',)

    # เพิ่มความสามารถในการค้นหาข้อมูล
    search_fields = ('code',)

    # เพิ่มความสามารถในการเรียงลำดับข้อมูล
    list_per_page = 20
    ordering = ('-valid_to',)

# สำหรับ ReviewRatingAdmin เราจะใช้ list_display เพื่อเลือกแสดงข้อมูลที่ต้องการในรายการ
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'review', 'status', 'created_at')

    # เพิ่มความสามารถในการกรองข้อมูล
    list_filter = ('status', 'rating')

    # เพิ่มความสามารถในการค้นหาข้อมูล
    search_fields = ('user__username', 'product__product_name')

    # เพิ่มความสามารถในการเรียงลำดับข้อมูล
    list_per_page = 20
    ordering = ('-created_at',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(Coupon, CouponAdmin)
