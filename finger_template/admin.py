from django.contrib import admin
from .models import template_info


class template_info_admin(admin.ModelAdmin):
    list_display = ['company_name', 'group_id', 'temp_id', 'temp']
    list_filter = ['company_name', 'group_id']
    search_fields = ['company_name', 'group_id', 'temp_id', 'temp']
    list_per_page = 20
admin.site.register(template_info, template_info_admin)

