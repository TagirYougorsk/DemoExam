from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'role', 'phone', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('name', 'phone', 'login')}),
        ('Права доступа', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'login', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'description_short')
    search_fields = ('name', 'serial_number')
    list_per_page = 20

    def description_short(self, obj):
        return obj.description[ :50 ] + '...' if len(obj.description) > 50 else obj.description

    description_short.short_description = 'Описание'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('autor', 'text', 'created_at')
    can_delete = False


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'equipment', 'status', 'created_at', 'completion_date')
    list_filter = ('status', 'created_at', 'completion_date')
    search_fields = ('number', 'client__name', 'equipment__name')
    readonly_fields = ('number', 'created_at')
    inlines = [ CommentInline ]
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('number', 'client', 'equipment', 'status')
        }),
        ('Детали заявки', {
            'fields': ('fault_type', 'description', 'assigned_to', 'manager')
        }),
        ('Даты', {
            'fields': ('created_at', 'completion_date')
        }),
        ('Дополнительно', {
            'fields': ('feedback',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('autor', 'repair_request', 'created_at', 'text_short')
    list_filter = ('created_at', 'autor')
    search_fields = ('text', 'autor__name', 'repair_request__number')

    def text_short(self, obj):
        return obj.text[ :50 ] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_description = 'Комментарий'


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('repair_request', 'changed_by', 'changed_at', 'change_short')
    list_filter = ('changed_at', 'changed_by')
    readonly_fields = ('changed_at',)

    def change_short(self, obj):
        return obj.change_description[ :50 ] + '...' if len(obj.change_description) > 50 else obj.change_description

    change_short.short_description = 'Изменения'