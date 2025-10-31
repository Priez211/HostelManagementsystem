from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Staff(models.Model):
    """Staff model representing hostel staff members"""
    CATEGORY_CHOICES = [
        ('ADMINISTRATIVE', 'Administrative'),
        ('HOUSEKEEPING', 'Housekeeping'),
        ('MAINTENANCE', 'Maintenance'),
        ('KITCHEN', 'Kitchen'),
        ('SECURITY', 'Security'),
    ]
    
    staff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ADMINISTRATIVE')
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff'
        verbose_name_plural = 'Staff'

    def __str__(self):
        return f"{self.name} - {self.role}"


class HostelBlock(models.Model):
    """Hostel block model representing different blocks in the hostel"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('MIXED', 'Mixed'),
    ]
    
    block_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    capacity = models.PositiveIntegerField()
    warden = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_blocks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hostel_block'
        verbose_name_plural = 'Hostel Blocks'

    def __str__(self):
        return f"{self.block_name} - {self.get_gender_display()}"


class Room(models.Model):
    """Room model representing individual rooms in the hostel"""
    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('TRIPLE', 'Triple'),
        ('QUAD', 'Quad'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('RESERVED', 'Reserved'),
    ]
    
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    occupants = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE')
    booked = models.BooleanField(default=False)
    block = models.ForeignKey(HostelBlock, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f"Room {self.room_number} - {self.get_room_type_display()}"


class Student(models.Model):
    """Student model representing hostel residents"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
        (5, 'Fifth Year'),
    ]
    
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=100)
    year_of_study = models.PositiveIntegerField(choices=YEAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.name} - {self.course} Year {self.year_of_study}"


class Fee(models.Model):
    """Fee model representing student fees"""
    FEE_TYPE_CHOICES = [
        ('ACCOMMODATION', 'Accommodation'),
        ('BOOKING', 'Booking'),
        ('MAINTENANCE', 'Maintenance'),
        ('SECURITY', 'Security'),
        ('UTILITIES', 'Utilities'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    fee_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_due = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fee'
        verbose_name_plural = 'Fees'

    def __str__(self):
        return f"{self.student.name} - {self.get_fee_type_display()} - ${self.amount}"


class DisciplinaryRecord(models.Model):
    """Disciplinary record model for tracking student violations"""
    VIOLATION_CHOICES = [
        ('NOISE', 'Excessive Noise'),
        ('DAMAGE', 'Property Damage'),
        ('LATE_NIGHT', 'Late Night Activity'),
        ('GUEST_VIOLATION', 'Guest Policy Violation'),
        ('CLEANLINESS', 'Room Cleanliness'),
        ('OTHER', 'Other'),
    ]
    
    record_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='disciplinary_records')
    date = models.DateField()
    violation = models.CharField(max_length=20, choices=VIOLATION_CHOICES)
    advice_taken = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'disciplinary_record'
        verbose_name_plural = 'Disciplinary Records'

    def __str__(self):
        return f"{self.student.name} - {self.get_violation_display()} - {self.date}"


class Visitor(models.Model):
    """Visitor model for tracking hostel visitors"""
    RELATIONSHIP_CHOICES = [
        ('PARENT', 'Parent'),
        ('SIBLING', 'Sibling'),
        ('FRIEND', 'Friend'),
        ('RELATIVE', 'Relative'),
        ('OTHER', 'Other'),
    ]
    
    visitor_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='visitors')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    visit_date = models.DateField()
    relationship_to_student = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES)
    purpose_of_visit = models.TextField()
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visitor'
        verbose_name_plural = 'Visitors'

    def __str__(self):
        return f"{self.name} visiting {self.student.name}"


class Allocation(models.Model):
    """Allocation model for room assignments"""
    allocation_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    date_allocated = models.DateField()
    date_vacated = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'allocation'
        verbose_name_plural = 'Allocations'
        unique_together = ['student', 'room', 'date_allocated']

    def __str__(self):
        return f"{self.student.name} - Room {self.room.room_number}"


class Booking(models.Model):
    """Booking model for room reservations"""
    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('TRIPLE', 'Triple'),
        ('QUAD', 'Quad'),
    ]
    
    booking_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='bookings')
    date_of_booking = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"Booking {self.booking_id} - Room {self.room.room_number}"


class Inventory(models.Model):
    """Inventory model for tracking room items"""
    ITEM_TYPE_CHOICES = [
        ('FURNITURE', 'Furniture'),
        ('ELECTRONICS', 'Electronics'),
        ('APPLIANCES', 'Appliances'),
        ('DECORATION', 'Decoration'),
        ('OTHER', 'Other'),
    ]
    
    CONDITION_CHOICES = [
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
        ('DAMAGED', 'Damaged'),
    ]
    
    item_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='inventory_items')
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=15, choices=ITEM_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory'
        verbose_name_plural = 'Inventory Items'

    def __str__(self):
        return f"{self.item_name} in Room {self.room.room_number}"


class MaintenanceRequest(models.Model):
    """Maintenance request model for room repairs"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    request_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests')
    handled_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_requests')
    description = models.TextField()
    request_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    completion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maintenance_request'
        verbose_name_plural = 'Maintenance Requests'

    def __str__(self):
        return f"Maintenance Request {self.request_id} - Room {self.room.room_number}"