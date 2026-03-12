from django.contrib import admin
from .models import Role

# Register your models here.

admin.site.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display  = ['name', 'code']
    search_fields = ['name', 'code']
    ordering      = ['name']