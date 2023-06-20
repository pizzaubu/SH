from django.contrib import admin
from .models import Payment, Order, OrderProduct, Refund
# Register your models here.


class OrderProductAdmin(admin.ModelAdmin):
    model = OrderProduct
    list_display = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    list_filter = ('ordered',)
    search_fields = ('created_at','updated_at')
    list_per_page = 20
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'city', 'order_total', 'tax', 'order_status', 'created_at','is_ordered')
    list_filter = ('order_status',)
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_per_page = 20

class RefundAdmin(admin.ModelAdmin):
    list_display = ['order', 'reason', 'accepted', 'email']
    list_filter = ['accepted', 'order']
    search_fields = ['order__order_number', 'email']
    list_per_page = 20

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','payment_id','payment_method','amount_paid','status']
    list_filter = ['payment_method', 'status']
    search_fields = ['user','payment_id']
    list_per_page = 20


admin.site.register(Refund, RefundAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
