from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)  # ชื่อหมวดหมู่
    slug = models.SlugField(max_length=100, unique=True)  # Slug สำหรับ SEO-friendly URL
    description = models.TextField(max_length=255, blank=True)  # คำอธิบายหมวดหมู่ (ถ้ามี)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)  # รูปภาพหมวดหมู่ (ถ้ามี)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        # สำหรับสร้าง URL ของหมวดหมู่สินค้า
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
