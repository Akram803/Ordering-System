from django.contrib import admin
from .models import Item, Category, AnonymouseOrder, CustomerOrder
# Register your models here.
admin.site.register(Category)
admin.site.register(AnonymouseOrder)
admin.site.register(CustomerOrder)



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price' )
    list_filter = ('availability', 'category')
#     # fields = [('availability', 'quantity')]