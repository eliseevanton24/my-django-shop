# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import ProductVariant  # ✅ Только Variant нужен
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)

    # получаем выбранный вариант (например, размер)
    variant_id = request.POST.get('variant_id')
    variant = get_object_or_404(ProductVariant, id=variant_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # добавляем в корзину ВАРИАНТ, не Product
        cart.add(product=variant, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)  # ✅ исправлено: ищем Variant
    cart.remove(variant)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )

    coupon_apply_form = CouponApplyForm()

    return render(
        request,
        'cart/detail.html',
        {
            'cart': cart,
            'coupon_apply_form': coupon_apply_form
        }
    )