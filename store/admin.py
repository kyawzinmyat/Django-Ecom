from django.contrib import admin

# Register your models here.
from .models import Products, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug' : ('name', )}

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price', 'is_active', 'in_stock', 'created', 'updated']
    list_filter = ['is_active', 'in_stock']
    prepopulated = {'slug' : ('title', )}
    list_editable = ['price', 'in_stock']