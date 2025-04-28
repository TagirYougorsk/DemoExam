from xmlrpc.client import Fault

from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'role', 'is_active', 'is_staff')
    search_fields = ('email', 'name', 'role')
    list_filter = ('role', 'is_active')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'serial_number')
    search_fields = ('name', 'serial_number')

@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'client', 'equipment', 'fault_type', 'description', 'status', 'assigned_to')
    search_fields = ('equipment__name', 'client__name', 'assigned_to__name')
    list_filter = ('status', 'created_at', 'completion_date')
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'repair_request', 'autor', 'created_at')
    search_fields = ('repair_request__id', 'autor__name')

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'repair_request', 'changed_by', 'changed_at')
    search_fields = ('repair_request__id', 'changed_by__name')
