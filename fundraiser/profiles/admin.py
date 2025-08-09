from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstname', 'lastname', 'email', 'user_type', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['phone_number', 'email', 'national_id']
    ordering = ['id']
    readonly_fields = ['id', 'date_joined', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'national_id', 'phone_number', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
@admin.register(Campaign_Owner)
class Campaign_OwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization_name', 'organization_description', 'organization_website', 'organization_logo', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__firstname', 'user__lastname', 'organization_name']
    ordering = ['user__id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__firstname', 'user__lastname']
    ordering = ['user__id']
    readonly_fields = ['created_at', 'updated_at']