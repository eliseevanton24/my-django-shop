from django.contrib import admin
from .models import Category, Product, ProductVariant

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

# Inline для отображения и редактирования вариантов товара (размеров, цен, остатков)
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_price', 'get_stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]

    def get_price(self, obj):
        variant = obj.variants.first()
        return variant.price if variant else '-'
    get_price.short_description = 'Цена'

    def get_stock(self, obj):
        variant = obj.variants.first()
        return variant.stock if variant else '-'
    get_stock.short_description = 'Остаток'

admin.site.register(Product, ProductAdmin)