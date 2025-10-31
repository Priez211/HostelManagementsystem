from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Staff, HostelBlock, Room, Student, Fee, DisciplinaryRecord,
    Visitor, Allocation, Booking, Inventory, MaintenanceRequest
)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'name', 'category', 'role', 'phone', 'email', 'salary', 'created_at']
    list_filter = ['category', 'role', 'created_at']
    search_fields = ['name', 'email', 'phone']
    ordering = ['name']
    readonly_fields = ['staff_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'role', 'phone', 'email')
        }),
        ('Financial', {
            'fields': ('salary',)
        }),
        ('System Information', {
            'fields': ('staff_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HostelBlock)
class HostelBlockAdmin(admin.ModelAdmin):
    list_display = ['block_id', 'block_name', 'gender', 'capacity', 'warden_link', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['block_name', 'warden__name']
    ordering = ['block_name']
    readonly_fields = ['block_id', 'created_at', 'updated_at']
    
    def warden_link(self, obj):
        if obj.warden:
            url = reverse('admin:core_staff_change', args=[obj.warden.staff_id])
            return format_html('<a href="{}">{}</a>', url, obj.warden.name)
        return '-'
    warden_link.short_description = 'Warden'
    
    fieldsets = (
        ('Block Information', {
            'fields': ('block_name', 'gender', 'capacity')
        }),
        ('Management', {
            'fields': ('warden',)
        }),
        ('System Information', {
            'fields': ('block_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'room_number', 'room_type', 'occupants', 'status', 'booked', 'block_link', 'created_at']
    list_filter = ['room_type', 'status', 'booked', 'block__block_name', 'created_at']
    search_fields = ['room_number', 'block__block_name']
    ordering = ['room_number']
    readonly_fields = ['room_id', 'created_at', 'updated_at']
    
    def block_link(self, obj):
        url = reverse('admin:core_hostelblock_change', args=[obj.block.block_id])
        return format_html('<a href="{}">{}</a>', url, obj.block.block_name)
    block_link.short_description = 'Block'
    
    fieldsets = (
        ('Room Information', {
            'fields': ('room_number', 'room_type', 'occupants', 'status', 'booked')
        }),
        ('Location', {
            'fields': ('block',)
        }),
        ('System Information', {
            'fields': ('room_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'course', 'year_of_study', 'gender', 'phone', 'email', 'created_at']
    list_filter = ['gender', 'year_of_study', 'course', 'created_at']
    search_fields = ['name', 'email', 'phone', 'course']
    ordering = ['name']
    readonly_fields = ['student_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'date_of_birth', 'gender', 'phone', 'email')
        }),
        ('Academic Information', {
            'fields': ('course', 'year_of_study')
        }),
        ('System Information', {
            'fields': ('student_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['fee_id', 'student_link', 'fee_type', 'amount', 'date_due', 'status', 'payment_date', 'created_at']
    list_filter = ['fee_type', 'status', 'date_due', 'created_at']
    search_fields = ['student__name', 'student__email']
    ordering = ['-created_at']
    readonly_fields = ['fee_id', 'created_at', 'updated_at']
    
    def student_link(self, obj):
        url = reverse('admin:core_student_change', args=[obj.student.student_id])
        return format_html('<a href="{}">{}</a>', url, obj.student.name)
    student_link.short_description = 'Student'
    
    fieldsets = (
        ('Fee Information', {
            'fields': ('student', 'fee_type', 'amount', 'date_due', 'status', 'payment_date')
        }),
        ('System Information', {
            'fields': ('fee_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DisciplinaryRecord)
class DisciplinaryRecordAdmin(admin.ModelAdmin):
    list_display = ['record_id', 'student_link', 'date', 'violation', 'created_at']
    list_filter = ['violation', 'date', 'created_at']
    search_fields = ['student__name', 'advice_taken']
    ordering = ['-date']
    readonly_fields = ['record_id', 'created_at', 'updated_at']
    
    def student_link(self, obj):
        url = reverse('admin:core_student_change', args=[obj.student.student_id])
        return format_html('<a href="{}">{}</a>', url, obj.student.name)
    student_link.short_description = 'Student'
    
    fieldsets = (
        ('Record Information', {
            'fields': ('student', 'date', 'violation', 'advice_taken')
        }),
        ('System Information', {
            'fields': ('record_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['visitor_id', 'name', 'student_link', 'visit_date', 'relationship_to_student', 'check_in_time', 'check_out_time']
    list_filter = ['relationship_to_student', 'visit_date', 'created_at']
    search_fields = ['name', 'student__name', 'phone']
    ordering = ['-visit_date']
    readonly_fields = ['visitor_id', 'created_at', 'updated_at']
    
    def student_link(self, obj):
        url = reverse('admin:core_student_change', args=[obj.student.student_id])
        return format_html('<a href="{}">{}</a>', url, obj.student.name)
    student_link.short_description = 'Student'
    
    fieldsets = (
        ('Visitor Information', {
            'fields': ('name', 'phone', 'relationship_to_student', 'purpose_of_visit')
        }),
        ('Visit Details', {
            'fields': ('student', 'visit_date', 'check_in_time', 'check_out_time')
        }),
        ('System Information', {
            'fields': ('visitor_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ['allocation_id', 'student_link', 'room_link', 'date_allocated', 'date_vacated', 'is_active', 'created_at']
    list_filter = ['is_active', 'date_allocated', 'created_at']
    search_fields = ['student__name', 'room__room_number']
    ordering = ['-date_allocated']
    readonly_fields = ['allocation_id', 'created_at', 'updated_at']
    
    def student_link(self, obj):
        url = reverse('admin:core_student_change', args=[obj.student.student_id])
        return format_html('<a href="{}">{}</a>', url, obj.student.name)
    student_link.short_description = 'Student'
    
    def room_link(self, obj):
        url = reverse('admin:core_room_change', args=[obj.room.room_id])
        return format_html('<a href="{}">{}</a>', url, obj.room.room_number)
    room_link.short_description = 'Room'
    
    fieldsets = (
        ('Allocation Information', {
            'fields': ('student', 'room', 'date_allocated', 'date_vacated', 'is_active')
        }),
        ('System Information', {
            'fields': ('allocation_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'room_link', 'student_link', 'date_of_booking', 'amount_paid', 'room_type', 'created_at']
    list_filter = ['room_type', 'date_of_booking', 'created_at']
    search_fields = ['room__room_number', 'fee__student__name']
    ordering = ['-date_of_booking']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    
    def room_link(self, obj):
        url = reverse('admin:core_room_change', args=[obj.room.room_id])
        return format_html('<a href="{}">{}</a>', url, obj.room.room_number)
    room_link.short_description = 'Room'
    
    def student_link(self, obj):
        url = reverse('admin:core_student_change', args=[obj.fee.student.student_id])
        return format_html('<a href="{}">{}</a>', url, obj.fee.student.name)
    student_link.short_description = 'Student'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('room', 'fee', 'date_of_booking', 'amount_paid', 'room_type')
        }),
        ('System Information', {
            'fields': ('booking_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'item_name', 'item_type', 'quantity', 'condition', 'room_link', 'created_at']
    list_filter = ['item_type', 'condition', 'room__block__block_name', 'created_at']
    search_fields = ['item_name', 'room__room_number']
    ordering = ['item_name']
    readonly_fields = ['item_id', 'created_at', 'updated_at']
    
    def room_link(self, obj):
        url = reverse('admin:core_room_change', args=[obj.room.room_id])
        return format_html('<a href="{}">{}</a>', url, obj.room.room_number)
    room_link.short_description = 'Room'
    
    fieldsets = (
        ('Item Information', {
            'fields': ('item_name', 'item_type', 'quantity', 'condition')
        }),
        ('Location', {
            'fields': ('room',)
        }),
        ('System Information', {
            'fields': ('item_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'room_link', 'description_short', 'request_date', 'status', 'handled_by_link', 'completion_date', 'created_at']
    list_filter = ['status', 'request_date', 'handled_by__role', 'created_at']
    search_fields = ['description', 'room__room_number', 'handled_by__name']
    ordering = ['-request_date']
    readonly_fields = ['request_id', 'created_at', 'updated_at']
    
    def room_link(self, obj):
        url = reverse('admin:core_room_change', args=[obj.room.room_id])
        return format_html('<a href="{}">{}</a>', url, obj.room.room_number)
    room_link.short_description = 'Room'
    
    def handled_by_link(self, obj):
        if obj.handled_by:
            url = reverse('admin:core_staff_change', args=[obj.handled_by.staff_id])
            return format_html('<a href="{}">{}</a>', url, obj.handled_by.name)
        return '-'
    handled_by_link.short_description = 'Handled By'
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('room', 'description', 'request_date', 'status', 'completion_date')
        }),
        ('Assignment', {
            'fields': ('handled_by',)
        }),
        ('System Information', {
            'fields': ('request_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Customize admin site
admin.site.site_header = "Hostel Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "Welcome to Hostel Management System Administration"