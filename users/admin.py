from django.contrib import admin
from .models import Employee, Department

admin.site.register(Department)


@admin.register(Employee)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('dasic_user_data', 'department')
    # list_filter = ('availability', 'category')
#     # fields = [('availability', 'quantity')]