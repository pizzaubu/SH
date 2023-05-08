from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    
    subject = forms.CharField(
        required=True,
        widget=forms.widgets.Input(attrs={"class": "form-control"}),
        label="หัวข้อ"
        
    )
    review = forms.CharField(
        widget=forms.widgets.Textarea(attrs={"class": "form-control"}),
        label="รีวิว" 
    )
    rating = forms.FloatField(
        required=True,
        widget=forms.widgets.Select(attrs={"class": "form-select"}, choices=[("", "Please select rating"), (1,"1 star"),(2,"2 star"),(3,"3 star"), (4,"4 star"), (5,"5 star")]),
        label="คะแนน" 
    )
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

