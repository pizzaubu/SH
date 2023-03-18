from django.contrib import admin
from .models import Payment, Order, OrderProduct, Refund
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'city', 'order_total', 'tax', 'order_status', 'created_at')
    list_filter = ('order_status',)
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    list_per_page = 20

class RefundAdmin(admin.ModelAdmin):
    list_display = ['order', 'reason', 'accepted', 'email']
    list_filter = ['accepted', 'order']
    search_fields = ['order__order_number', 'email']
    list_per_page = 20

admin.site.register(Refund, RefundAdmin)
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
