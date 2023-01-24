from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.all_products, name = 'view_all'),
    path('product/<slug:slug>/', views.product_detail, name = "product_detail"),
    path('search/<slug:product_category>', views.category_list, name = 'category_list')
]