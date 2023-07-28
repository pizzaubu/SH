from django import forms
from accounts.models import Account
from store.models import Product
from category.models import Category

class AdminLoginForms(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class":"form-control","placeholder":"ชื่อผู้ใช้งาน" }),
        label="ชื่อผู้ใช้งาน"
    )

    password = forms.CharField(
        required=True,
        widget=forms.widgets.PasswordInput(attrs={"class":"form-control","placeholder":"รหัสผ่าน" }),
        label="รหัสผ่าน"
    )

    class Meta:
        model = Account
        fields = ['username','password']

class AddCategoryForms(forms.ModelForm):
    category_name = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class":"form-control","placeholder":"ชื่อหมวดหมู่"}),
        label="ชื่อหมวดหมู่"
    )

    slug = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class":"form-control","placeholder":"slug"}),
        label="slug"
    )

    class Meta:
        model = Category
        fields = ['category_name','slug']