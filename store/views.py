from django.shortcuts import render, get_object_or_404
from .models import Products, Category
# Create your views here.

def all_products(request):
    products = Products.products.all()
    return render(request, 'Templates/store/home.html', {
        'products' : products
    })

def product_detail(request, slug):
    product = get_object_or_404(Products, slug = slug, in_stock = True)
    return render(request, 'store/product_detail.html', {
                'product': product
    })

def category_list(request, product_category):
    category = get_object_or_404(Category, slug = product_category)
    products = Products.objects.filter(category = category)
    return render(request, 'store/category_list.html', {'products': products, 'category': category})