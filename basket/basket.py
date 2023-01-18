from store.models import Products
from decimal import Decimal



class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in self.session:
            basket = self.session['skey'] = {}
        self.basket = basket
    
    def __iter__(self):
        product_ids = self.basket.keys()
        product_objs = Products.products.filter(id__in = product_ids)
        basket = self.basket.copy()
        for product_obj in product_objs:
            basket[str(product_obj.id)]['product'] = product_obj
        # self.basket = {'1' : {'price' : 10}}
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def save(self):
        self.session.modified = True
    
    def delete(self, product_id):
        product_id = str(product_id)
        print(product_id in self.basket)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty': product_qty}
        else:
            self.basket[product_id]['qty'] = self.basket[product_id]['qty'] + product_qty
        self.save()

    def get_qty(self):
        return sum(item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(product['price'] * product['qty'] for product in self.basket.values())
    
    def __len__(self):
        return self.get_qty()