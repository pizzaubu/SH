from django import forms
from .models import Order,Refund

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class": "form-control", "placeholder": "ชื่อ"}),
        label="ชื่อ"
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class": "form-control", "placeholder": "นามสกุล"}),
        label="นามสกุล"
    )

    phone = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class": "form-control", "placeholder": "หมายเลขโทรศัพท์"}),
        label="หมายเลขโทรศัพท์"
    )

    email = forms.EmailField(
        required=True,
        widget=forms.widgets.Input(attrs={"class": "form-control", "placeholder": "อีเมล"}),
        label="อีเมล"
    )

    address_line_1 = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class": "form-control", "placeholder": "ที่อยู่ 1"}),
        label="ที่อยู่ 1"
    )

    address_line_2 = forms.CharField(
        required=False,
        widget=forms.widgets.Input(attrs={"class": "form-control", "placeholder": "ที่อยู่ 2"}),
        label="ที่อยู่ 2"
    )

    state = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class": "form-control", "placeholder": "จังหวัด"}),
        label="จังหวัด"
    )

    order_note = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(attrs={"class": "form-control", "placeholder": "ข้อความเพิ่มเติม"}),
        label="ข้อความเพิ่มเติม"
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'state', 'order_note']


class ReturnForm(forms.ModelForm):

    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Order"
    )

    reason = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "เหตุผลในการคืนสินค้า"}),
        label="Reason"
    )

    class Meta:
        model = Refund
        fields = ['order', 'reason']