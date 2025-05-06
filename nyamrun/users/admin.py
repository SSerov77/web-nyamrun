from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('name', 'email')}),
        ('Статус', {'fields': ('is_owner',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_owner')}
        ),
    )
    list_display = ('username', 'email', 'name', 'is_owner', 'is_staff')
    list_filter = ('is_owner', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'name')
    ordering = ('username',)
