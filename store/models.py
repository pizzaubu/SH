from django.db import models
from category.models import Category
from accounts.models import Account
from django.urls import reverse
from django.db.models import Avg, Count
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.utils import timezone

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(choices=[(1,"1 star"),(2,"2 star"),(3,"3 star"), (4,"4 star"), (5,"5 star")])
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    
    def get_coupon(self, code): # code = 6877725454
        try:
            coupon = Coupon.objects.get(code=code)
            """
                coupon = {
                    code: 6877725454
                    valid_from: April 29, 2023, 8:13 a.m.
                    valid_to:
                    discount:
                    is_active:
                }
            """
            if coupon.is_active and (coupon.valid_from <= timezone.now()) and (coupon.valid_to >= timezone.now()):
                return coupon
            else:
                return None
        except Coupon.DoesNotExist:
            return None


