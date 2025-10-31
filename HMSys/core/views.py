from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, date, timedelta
from collections import defaultdict
import json

from .models import (
    Staff, HostelBlock, Room, Student, Fee, DisciplinaryRecord,
    Visitor, Allocation, Booking, Inventory, MaintenanceRequest
)


def frontend(request):
    """Serve the frontend application"""
    return render(request, 'index.html')


# Staff Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def staff_list(request):
    """List all staff members or create a new one"""
    if request.method == 'GET':
        staff_members = Staff.objects.all().order_by('name')
        paginator = Paginator(staff_members, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        data = {
            'staff': [{
                'staff_id': staff.staff_id,
                'name': staff.name,
                'category': staff.category,
                'role': staff.role,
                'phone': staff.phone,
                'email': staff.email,
                'salary': float(staff.salary),
                'created_at': staff.created_at.isoformat(),
            } for staff in page_obj]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Check if email already exists
            if Staff.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'A staff member with this email already exists'}, status=400)
            
            staff = Staff.objects.create(
                name=data['name'],
                category=data['category'],
                role=data['role'],
                phone=data['phone'],
                email=data['email'],
                salary=data['salary']
            )
            return JsonResponse({
                'staff_id': staff.staff_id,
                'message': 'Staff member created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_exempt
def staff_detail(request, staff_id):
    """Get, update, or delete a specific staff member"""
    staff = get_object_or_404(Staff, staff_id=staff_id)
    
    if request.method == 'GET':
        data = {
            'staff_id': staff.staff_id,
            'name': staff.name,
            'category': staff.category,
            'role': staff.role,
            'phone': staff.phone,
            'email': staff.email,
            'salary': float(staff.salary),
            'created_at': staff.created_at.isoformat(),
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            staff.name = data.get('name', staff.name)
            staff.category = data.get('category', staff.category)
            staff.role = data.get('role', staff.role)
            staff.phone = data.get('phone', staff.phone)
            staff.email = data.get('email', staff.email)
            staff.salary = data.get('salary', staff.salary)
            staff.save()
            return JsonResponse({'message': 'Staff member updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        staff.delete()
        return JsonResponse({'message': 'Staff member deleted successfully'})


# Hostel Block Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def hostel_block_list(request):
    """List all hostel blocks or create a new one"""
    if request.method == 'GET':
        blocks = HostelBlock.objects.all().order_by('block_name')
        data = {
            'blocks': [{
                'block_id': block.block_id,
                'block_name': block.block_name,
                'gender': block.gender,
                'capacity': block.capacity,
                'warden': {
                    'staff_id': block.warden.staff_id,
                    'name': block.warden.name
                } if block.warden else None,
                'created_at': block.created_at.isoformat(),
            } for block in blocks]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            warden = None
            if 'warden_id' in data:
                warden = get_object_or_404(Staff, staff_id=data['warden_id'])
            
            block = HostelBlock.objects.create(
                block_name=data['block_name'],
                gender=data['gender'],
                capacity=data['capacity'],
                warden=warden
            )
            return JsonResponse({
                'block_id': block.block_id,
                'message': 'Hostel block created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Room Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def room_list(request):
    """List all rooms or create a new one"""
    if request.method == 'GET':
        rooms = Room.objects.select_related('block').all().order_by('room_number')
        data = {
            'rooms': [{
                'room_id': room.room_id,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'occupants': room.occupants,
                'status': room.status,
                'booked': room.booked,
                'block': {
                    'block_id': room.block.block_id,
                    'block_name': room.block.block_name
                },
                'created_at': room.created_at.isoformat(),
            } for room in rooms]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            block = get_object_or_404(HostelBlock, block_id=data['block_id'])
            room = Room.objects.create(
                room_number=data['room_number'],
                room_type=data['room_type'],
                occupants=data.get('occupants', 0),
                status=data.get('status', 'AVAILABLE'),
                booked=data.get('booked', False),
                block=block
            )
            return JsonResponse({
                'room_id': room.room_id,
                'message': 'Room created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Student Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def student_list(request):
    """List all students or create a new one"""
    if request.method == 'GET':
        students = Student.objects.all().order_by('name')
        paginator = Paginator(students, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        data = {
            'students': [{
                'student_id': student.student_id,
                'name': student.name,
                'date_of_birth': student.date_of_birth.isoformat(),
                'gender': student.gender,
                'phone': student.phone,
                'email': student.email,
                'course': student.course,
                'year_of_study': student.year_of_study,
                # include current allocation (room) and fee payment status
                'room_number': (Allocation.objects.filter(student=student, is_active=True).select_related('room').first().room.room_number
                                if Allocation.objects.filter(student=student, is_active=True).select_related('room').exists() else None),
                'fee_status': ('PENDING' if Fee.objects.filter(student=student, status='PENDING').exists() else 'PAID'),
                'created_at': student.created_at.isoformat(),
            } for student in page_obj]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Check if email already exists
            if Student.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'A student with this email already exists'}, status=400)
            
            student = Student.objects.create(
                name=data['name'],
                date_of_birth=data['date_of_birth'],
                gender=data['gender'],
                phone=data['phone'],
                email=data['email'],
                course=data['course'],
                year_of_study=data['year_of_study']
            )
            return JsonResponse({
                'student_id': student.student_id,
                'message': 'Student created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_exempt
def student_detail(request, student_id):
    """Get, update, or delete a specific student"""
    student = get_object_or_404(Student, student_id=student_id)
    
    if request.method == 'GET':
        data = {
            'student_id': student.student_id,
            'name': student.name,
            'date_of_birth': student.date_of_birth.isoformat(),
            'gender': student.gender,
            'phone': student.phone,
            'email': student.email,
            'course': student.course,
            'year_of_study': student.year_of_study,
            'created_at': student.created_at.isoformat(),
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            student.name = data.get('name', student.name)
            student.date_of_birth = data.get('date_of_birth', student.date_of_birth)
            student.gender = data.get('gender', student.gender)
            student.phone = data.get('phone', student.phone)
            student.email = data.get('email', student.email)
            student.course = data.get('course', student.course)
            student.year_of_study = data.get('year_of_study', student.year_of_study)
            student.save()
            return JsonResponse({'message': 'Student updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully'})


# Fee Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def fee_list(request):
    """List all fees or create a new one"""
    if request.method == 'GET':
        fees = Fee.objects.select_related('student').all().order_by('-created_at')
        data = {
            'fees': [{
                'fee_id': fee.fee_id,
                'student': {
                    'student_id': fee.student.student_id,
                    'name': fee.student.name
                },
                'fee_type': fee.fee_type,
                'amount': float(fee.amount),
                'date_due': fee.date_due.isoformat(),
                'status': fee.status,
                'payment_date': fee.payment_date.isoformat() if fee.payment_date else None,
                'created_at': fee.created_at.isoformat(),
            } for fee in fees]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, student_id=data['student_id'])
            fee = Fee.objects.create(
                student=student,
                fee_type=data['fee_type'],
                amount=data['amount'],
                date_due=data['date_due'],
                status=data.get('status', 'PENDING')
            )
            return JsonResponse({
                'fee_id': fee.fee_id,
                'message': 'Fee created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Disciplinary Record Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def disciplinary_record_list(request):
    """List all disciplinary records or create a new one"""
    if request.method == 'GET':
        records = DisciplinaryRecord.objects.select_related('student').all().order_by('-date')
        data = {
            'records': [{
                'record_id': record.record_id,
                'student': {
                    'student_id': record.student.student_id,
                    'name': record.student.name
                },
                'date': record.date.isoformat(),
                'violation': record.violation,
                'advice_taken': record.advice_taken,
                'created_at': record.created_at.isoformat(),
            } for record in records]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, student_id=data['student_id'])
            record = DisciplinaryRecord.objects.create(
                student=student,
                date=data['date'],
                violation=data['violation'],
                advice_taken=data['advice_taken']
            )
            return JsonResponse({
                'record_id': record.record_id,
                'message': 'Disciplinary record created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Visitor Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def visitor_list(request):
    """List all visitors or create a new one"""
    if request.method == 'GET':
        visitors = Visitor.objects.select_related('student').all().order_by('-visit_date')
        data = {
            'visitors': [{
                'visitor_id': visitor.visitor_id,
                'student': {
                    'student_id': visitor.student.student_id,
                    'name': visitor.student.name
                },
                'name': visitor.name,
                'phone': visitor.phone,
                'visit_date': visitor.visit_date.isoformat(),
                'relationship_to_student': visitor.relationship_to_student,
                'purpose_of_visit': visitor.purpose_of_visit,
                'check_in_time': visitor.check_in_time.isoformat(),
                'check_out_time': visitor.check_out_time.isoformat() if visitor.check_out_time else None,
                'created_at': visitor.created_at.isoformat(),
            } for visitor in visitors]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, student_id=data['student_id'])
            visitor = Visitor.objects.create(
                student=student,
                name=data['name'],
                phone=data['phone'],
                visit_date=data['visit_date'],
                relationship_to_student=data['relationship_to_student'],
                purpose_of_visit=data['purpose_of_visit'],
                check_in_time=data['check_in_time']
            )
            return JsonResponse({
                'visitor_id': visitor.visitor_id,
                'message': 'Visitor record created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Allocation Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def allocation_list(request):
    """List all allocations or create a new one"""
    if request.method == 'GET':
        allocations = Allocation.objects.select_related('student', 'room').all().order_by('-date_allocated')
        data = {
            'allocations': [{
                'allocation_id': allocation.allocation_id,
                'student': {
                    'student_id': allocation.student.student_id,
                    'name': allocation.student.name
                },
                'room': {
                    'room_id': allocation.room.room_id,
                    'room_number': allocation.room.room_number
                },
                'date_allocated': allocation.date_allocated.isoformat(),
                'date_vacated': allocation.date_vacated.isoformat() if allocation.date_vacated else None,
                'is_active': allocation.is_active,
                'created_at': allocation.created_at.isoformat(),
            } for allocation in allocations]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = get_object_or_404(Student, student_id=data['student_id'])
            room = get_object_or_404(Room, room_id=data['room_id'])
            allocation = Allocation.objects.create(
                student=student,
                room=room,
                date_allocated=data['date_allocated'],
                is_active=data.get('is_active', True)
            )
            return JsonResponse({
                'allocation_id': allocation.allocation_id,
                'message': 'Allocation created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Booking Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def booking_list(request):
    """List all bookings or create a new one"""
    if request.method == 'GET':
        bookings = Booking.objects.select_related('room', 'fee__student').all().order_by('-date_of_booking')
        data = {
            'bookings': [{
                'booking_id': booking.booking_id,
                'room': {
                    'room_id': booking.room.room_id,
                    'room_number': booking.room.room_number
                },
                'fee': {
                    'fee_id': booking.fee.fee_id,
                    'student': {
                        'student_id': booking.fee.student.student_id,
                        'name': booking.fee.student.name
                    }
                },
                'date_of_booking': booking.date_of_booking.isoformat(),
                'amount_paid': float(booking.amount_paid),
                'room_type': booking.room_type,
                'created_at': booking.created_at.isoformat(),
            } for booking in bookings]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            room = get_object_or_404(Room, room_id=data['room_id'])
            fee = get_object_or_404(Fee, fee_id=data['fee_id'])
            booking = Booking.objects.create(
                room=room,
                fee=fee,
                date_of_booking=data['date_of_booking'],
                amount_paid=data['amount_paid'],
                room_type=data['room_type']
            )
            return JsonResponse({
                'booking_id': booking.booking_id,
                'message': 'Booking created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Inventory Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def inventory_list(request):
    """List all inventory items or create a new one"""
    if request.method == 'GET':
        inventory_items = Inventory.objects.select_related('room').all().order_by('item_name')
        data = {
            'inventory': [{
                'item_id': item.item_id,
                'room': {
                    'room_id': item.room.room_id,
                    'room_number': item.room.room_number
                },
                'item_name': item.item_name,
                'item_type': item.item_type,
                'quantity': item.quantity,
                'condition': item.condition,
                'created_at': item.created_at.isoformat(),
            } for item in inventory_items]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            room = get_object_or_404(Room, room_id=data['room_id'])
            item = Inventory.objects.create(
                room=room,
                item_name=data['item_name'],
                item_type=data['item_type'],
                quantity=data['quantity'],
                condition=data['condition']
            )
            return JsonResponse({
                'item_id': item.item_id,
                'message': 'Inventory item created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Maintenance Request Views
@require_http_methods(["GET", "POST"])
@csrf_exempt
def maintenance_request_list(request):
    """List all maintenance requests or create a new one"""
    if request.method == 'GET':
        requests = MaintenanceRequest.objects.select_related('room', 'handled_by').all().order_by('-request_date')
        data = {
            'maintenance_requests': [{
                'request_id': req.request_id,
                'room': {
                    'room_id': req.room.room_id,
                    'room_number': req.room.room_number
                },
                'handled_by': {
                    'staff_id': req.handled_by.staff_id,
                    'name': req.handled_by.name
                } if req.handled_by else None,
                'description': req.description,
                'request_date': req.request_date.isoformat(),
                'status': req.status,
                'completion_date': req.completion_date.isoformat() if req.completion_date else None,
                'created_at': req.created_at.isoformat(),
            } for req in requests]
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            room = get_object_or_404(Room, room_id=data['room_id'])
            handled_by = None
            if 'handled_by_id' in data:
                handled_by = get_object_or_404(Staff, staff_id=data['handled_by_id'])
            
            request_obj = MaintenanceRequest.objects.create(
                room=room,
                handled_by=handled_by,
                description=data['description'],
                request_date=data['request_date'],
                status=data.get('status', 'PENDING')
            )
            return JsonResponse({
                'request_id': request_obj.request_id,
                'message': 'Maintenance request created successfully'
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Staff Category Views
@require_http_methods(["GET"])
def staff_by_category(request, category):
    """Get staff members by category"""
    try:
        staff_members = Staff.objects.filter(category=category.upper()).order_by('name')
        data = {
            'category': category,
            'staff': [{
                'staff_id': staff.staff_id,
                'name': staff.name,
                'category': staff.category,
                'role': staff.role,
                'phone': staff.phone,
                'email': staff.email,
                'salary': float(staff.salary),
                'created_at': staff.created_at.isoformat(),
            } for staff in staff_members]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def staff_categories(request):
    """Get all available staff categories"""
    try:
        categories = [{'value': choice[0], 'label': choice[1]} for choice in Staff.CATEGORY_CHOICES]
        return JsonResponse({'categories': categories})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Dashboard/Statistics Views
@require_http_methods(["GET"])
def dashboard_stats(request):
    """Get dashboard statistics"""
    try:
        stats = {
            'total_students': Student.objects.count(),
            'total_rooms': Room.objects.count(),
            'total_blocks': HostelBlock.objects.count(),
            'available_rooms': Room.objects.filter(status='AVAILABLE').count(),
            'occupied_rooms': Room.objects.filter(status='OCCUPIED').count(),
            'total_staff': Staff.objects.count(),
            'pending_fees': Fee.objects.filter(status='PENDING').count(),
            'pending_maintenance': MaintenanceRequest.objects.filter(status='PENDING').count(),
            'active_allocations': Allocation.objects.filter(is_active=True).count(),
            'collected_fees': float(Fee.objects.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or 0),
            'outstanding_fees': float(Fee.objects.filter(status='PENDING').aggregate(total=Sum('amount'))['total'] or 0),
        }
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def notifications(request):
    """Get notifications for the dashboard"""
    try:
        # Create sample notifications based on system data
        notifications_list = []
        
        # Overdue fees
        overdue_fees = Fee.objects.filter(
            status='PENDING',
            date_due__lt=timezone.now().date()
        ).count()
        if overdue_fees > 0:
            notifications_list.append({
                'id': 1,
                'type': 'warning',
                'title': 'Overdue Fees',
                'message': f'{overdue_fees} students have overdue fee payments',
                'timestamp': timezone.now().isoformat(),
                'read': False
            })
        
        # Pending maintenance requests
        pending_maintenance = MaintenanceRequest.objects.filter(status='PENDING').count()
        if pending_maintenance > 0:
            notifications_list.append({
                'id': 2,
                'type': 'info',
                'title': 'Maintenance Requests',
                'message': f'{pending_maintenance} maintenance requests pending',
                'timestamp': timezone.now().isoformat(),
                'read': False
            })
        
        # Room occupancy alerts
        high_occupancy_rooms = Room.objects.filter(
            status='OCCUPIED',
            occupants__gte=4
        ).count()
        if high_occupancy_rooms > 0:
            notifications_list.append({
                'id': 3,
                'type': 'success',
                'title': 'High Occupancy',
                'message': f'{high_occupancy_rooms} rooms at full capacity',
                'timestamp': timezone.now().isoformat(),
                'read': False
            })
        
        return JsonResponse({
            'notifications': notifications_list,
            'unread_count': len(notifications_list)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def user_info(request):
    """Get current user information"""
    try:
        # In a real application, this would get data from the authenticated user
        user_data = {
            'name': 'Admin User',
            'email': 'admin@hostelpro.com',
            'role': 'System Administrator',
            'avatar': 'https://via.placeholder.com/44',
            'last_login': timezone.now().isoformat(),
            'permissions': ['manage_students', 'manage_rooms', 'manage_staff', 'view_reports']
        }
        return JsonResponse(user_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Search Views
@require_http_methods(["GET"])
def search_students(request):
    """Search students by name, course, or email"""
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'students': []})
    
    students = Student.objects.filter(
        Q(name__icontains=query) |
        Q(course__icontains=query) |
        Q(email__icontains=query)
    )[:10]
    
    data = {
        'students': [{
            'student_id': student.student_id,
            'name': student.name,
            'course': student.course,
            'email': student.email,
            'year_of_study': student.year_of_study,
        } for student in students]
    }
    return JsonResponse(data)


@require_http_methods(["GET"])
def search_rooms(request):
    """Search rooms by number, type, or status"""
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'rooms': []})
    
    rooms = Room.objects.filter(
        Q(room_number__icontains=query) |
        Q(room_type__icontains=query) |
        Q(status__icontains=query)
    )[:10]
    
    data = {
        'rooms': [{
            'room_id': room.room_id,
            'room_number': room.room_number,
            'room_type': room.room_type,
            'status': room.status,
            'block_name': room.block.block_name,
        } for room in rooms]
    }
    return JsonResponse(data)


# Reports Views
@require_http_methods(["GET"])
def reports_data(request):
    """Get comprehensive reports data for charts and analytics"""
    try:
        # Calculate live stats
        total_students = Student.objects.count()
        total_rooms = Room.objects.count()
        total_staff = Staff.objects.count()

        occupied_rooms = Room.objects.filter(status='OCCUPIED').count()
        available_rooms = Room.objects.filter(status='AVAILABLE').count()
        maintenance_rooms = Room.objects.filter(status__icontains='MAINTENANCE').count()
        reserved_rooms = Room.objects.filter(status__icontains='RESERVED').count()

        # Fees aggregates
        total_fees_collected = float(Fee.objects.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or 0)
        total_pending_fees = float(Fee.objects.filter(status='PENDING').aggregate(total=Sum('amount'))['total'] or 0)

        # Occupancy rate (guard divide-by-zero)
        occupancy_rate = 0.0
        if total_rooms > 0:
            occupancy_rate = round((occupied_rooms / total_rooms) * 100, 1)

        # Room status pie data
        room_status_pie = {
            'labels': ['Available', 'Occupied', 'Under Maintenance', 'Reserved'],
            'data': [available_rooms, occupied_rooms, maintenance_rooms, reserved_rooms],
            'colors': ['#4CAF50', '#2196F3', '#FF9800', '#F44336']
        }

        # Fee payment trend: build a simple month series for the last 6 months
        today = timezone.now().date()
        months = []
        paid_series = []
        unpaid_series = []
        for i in range(5, -1, -1):
            start = (today.replace(day=1) - timedelta(days=1)).replace(day=1) - timedelta(days=0)
            # calculate target month by shifting properly
            target = (today.replace(day=1) - timedelta(days=30*i))
            label = target.strftime('%Y-%m')
            months.append(label)

            # Sum paid and unpaid in the month (using payment_date for paid, date_due for pending)
            month_start = target.replace(day=1)
            # approximate month end by adding month to next month start
            next_month = (month_start + timedelta(days=32)).replace(day=1)

            paid_amount = Fee.objects.filter(status='PAID', payment_date__gte=month_start, payment_date__lt=next_month).aggregate(total=Sum('amount'))['total'] or 0
            unpaid_amount = Fee.objects.filter(status='PENDING', date_due__gte=month_start, date_due__lt=next_month).aggregate(total=Sum('amount'))['total'] or 0

            paid_series.append(float(paid_amount))
            unpaid_series.append(float(unpaid_amount))

        fee_payment_line = {
            'labels': months,
            'datasets': [
                {
                    'label': 'Paid Fees',
                    'data': paid_series,
                    'borderColor': '#4CAF50',
                    'backgroundColor': 'rgba(76, 175, 80, 0.1)',
                    'tension': 0.4
                },
                {
                    'label': 'Unpaid Fees',
                    'data': unpaid_series,
                    'borderColor': '#F44336',
                    'backgroundColor': 'rgba(244, 67, 54, 0.1)',
                    'tension': 0.4
                }
            ]
        }

        reports_data = {
            'room_status_pie': room_status_pie,
            'fee_payment_line': fee_payment_line,
            'summary_stats': {
                'total_students': total_students,
                'total_rooms': total_rooms,
                'total_staff': total_staff,
                'total_fees_collected': total_fees_collected,
                'total_pending_fees': total_pending_fees,
                'occupancy_rate': occupancy_rate,
                'avg_fee_per_student': (total_fees_collected / total_students) if total_students > 0 else 0,
            }
        }

        return JsonResponse(reports_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)