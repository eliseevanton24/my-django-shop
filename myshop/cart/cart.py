from decimal import Decimal
from django.conf import settings
from shop.models import ProductVariant
from coupons.models import Coupon

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        variant_ids = [int(k) for k in self.cart.keys() if k.isdigit()]
        variants = ProductVariant.objects.select_related('product').filter(id__in=variant_ids)
        cart = self.cart.copy()
        for variant in variants:
            cart[str(variant.id)]['variant'] = variant  # 👈 вместо 'product'
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            if 'variant' in item:
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.pop('coupon_id', None)  # удаляем купон при очистке корзины
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                return None
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()