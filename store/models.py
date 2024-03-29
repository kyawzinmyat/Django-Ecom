from django.db import models
from django.urls import reverse
from django.conf import settings 
# Create your models here.

User = settings.AUTH_USER_MODEL

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active = True)

class Category(models.Model):
    name = models.CharField(max_length = 255, db_index = True)
    slug = models.SlugField(max_length = 255, unique = True)

    class Meta:
        verbose_name_plural = "categories"
    
    def get_absolute_url(self):
        return reverse("store:category_list", kwargs={"product_category": self.slug})
    

    def __str__(self):
        return self.name

class Products(models.Model):
    category = models.ForeignKey(Category, related_name = "product", on_delete = models.CASCADE)
    created_by = models.ForeignKey(User, related_name = "product_creator", on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255, default = "admin")
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = "images/", default = 'images/default_img.png')
    slug = models.SlugField(max_length = 255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField( auto_now = True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = "products"
        ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"slug": self.slug})
    

    def __repr__(self):
        return self.title