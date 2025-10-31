from django.urls import path
from . import views

urlpatterns = [
    # Frontend
    path('', views.frontend, name='frontend'),
    
    # Staff URLs
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('staff/category/<str:category>/', views.staff_by_category, name='staff_by_category'),
    path('staff/categories/', views.staff_categories, name='staff_categories'),
    
    # Hostel Block URLs
    path('blocks/', views.hostel_block_list, name='hostel_block_list'),
    
    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Fee URLs
    path('fees/', views.fee_list, name='fee_list'),
    
    # Disciplinary Record URLs
    path('disciplinary-records/', views.disciplinary_record_list, name='disciplinary_record_list'),
    
    # Visitor URLs
    path('visitors/', views.visitor_list, name='visitor_list'),
    
    # Allocation URLs
    path('allocations/', views.allocation_list, name='allocation_list'),
    
    # Booking URLs
    path('bookings/', views.booking_list, name='booking_list'),
    
    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory_list'),
    
    # Maintenance Request URLs
    path('maintenance-requests/', views.maintenance_request_list, name='maintenance_request_list'),
    
    # Dashboard and Search URLs
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('notifications/', views.notifications, name='notifications'),
    path('user/info/', views.user_info, name='user_info'),
    path('search/students/', views.search_students, name='search_students'),
    path('search/rooms/', views.search_rooms, name='search_rooms'),
    
    # Reports URLs
    path('reports/data/', views.reports_data, name='reports_data'),
]
