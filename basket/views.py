from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .basket import Basket
from store.models import Products

# Create your views here.
def basket_summary(request):
    return render(request, 'basket/basket_summary.html')

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product_obj = get_object_or_404(Products, id = product_id)
        basket.add(product = product_obj, product_qty = product_qty)  
        response = JsonResponse(
                {   
                    'product_id': product_id,
                    'qty': basket.get_qty(), 
                    'sub_total': basket.get_total_price(),
                    'product_qty': basket.get_product_qty(product_id)
                }
            )
        return response
    
def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))
        if basket.get_product_qty(product_id) - product_qty <0:
            return  JsonResponse({"error_message": "Not Enough products to remove!"}, status_code = 403)
        basket.delete(product_id, product_qty)   
        response = JsonResponse(
                {   
                    'product_id': product_id,
                    'qty': basket.get_qty(), 
                    'sub_total': basket.get_total_price(),
                    'product_qty': basket.get_product_qty(product_id)
                }
            )
        return response