from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'ป้อนรหัสผ่าน',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'ยืนยันรหัสผ่าน'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "รหัสผ่านไม่ตรงกัน!"
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'ป้อนชื่อจริง'
        self.fields['last_name'].widget.attrs['placeholder'] = 'ป้อนนามสกุล'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'ป้อนหมายเลขโทรศัพท์'
        self.fields['email'].widget.attrs['placeholder'] = 'ป้อนที่อยู่อีเมล'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
