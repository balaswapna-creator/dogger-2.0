# backend/clinic/monitoring.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from django.db import connection
import psutil
import time
from clinic.models import Patient, Owner, MedicalRecord, Vaccination, Prescription, Payment

@api_view(['GET'])
def health_check(request):
    """
    Public health check endpoint - no authentication required
    Returns overall system health status
    """
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Database check
    try:
        connection.ensure_connection()
        health_status['checks']['database'] = {
            'status': 'healthy',
            'type': connection.settings_dict['ENGINE'].split('.')[-1]
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = {'status': 'healthy'}
        else:
            health_status['checks']['cache'] = {'status': 'unhealthy'}
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['cache'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Disk space check
    try:
        disk = psutil.disk_usage('/')
        health_status['checks']['disk'] = {
            'status': 'healthy' if disk.percent < 90 else 'warning',
            'used_percent': disk.percent,
            'free_gb': round(disk.free / (1024**3), 2)
        }
    except Exception as e:
        health_status['checks']['disk'] = {
            'status': 'unknown',
            'error': str(e)
        }
    
    # Memory check
    try:
        memory = psutil.virtual_memory()
        health_status['checks']['memory'] = {
            'status': 'healthy' if memory.percent < 90 else 'warning',
            'used_percent': memory.percent,
            'available_gb': round(memory.available / (1024**3), 2)
        }
    except Exception as e:
        health_status['checks']['memory'] = {
            'status': 'unknown',
            'error': str(e)
        }
    
    # API performance check
    try:
        start_time = time.time()
        # Simple database query
        Patient.objects.count()
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        
        health_status['checks']['api_performance'] = {
            'status': 'healthy' if response_time < 1000 else 'slow',
            'response_time_ms': round(response_time, 2)
        }
    except Exception as e:
        health_status['checks']['api_performance'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    return Response(health_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_metrics(request):
    """
    Detailed system metrics - requires authentication
    Only accessible by admin, doctor, or staff users
    """
    user = request.user
    
    # UPDATED: Allow staff users or admin/doctor roles
    if not (user.is_staff or getattr(user, 'role', None) == 'admin' or getattr(user, 'role', None) == 'doctor'):
        return Response(
            {'error': 'Admin, doctor, or staff access required'},
            status=403
        )
    
    metrics = {}
    
    # System metrics
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory
        memory = psutil.virtual_memory()
        
        # Disk
        disk = psutil.disk_usage('/')
        
        metrics['system'] = {
            'cpu': {
                'usage_percent': cpu_percent,
                'cores': cpu_count
            },
            'memory': {
                'total_gb': round(memory.total / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'percent': memory.percent
            },
            'disk': {
                'total_gb': round(disk.total / (1024**3), 2),
                'used_gb': round(disk.used / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'percent': disk.percent
            }
        }
    except Exception as e:
        metrics['system'] = {'error': str(e)}
    
    # Database metrics
    try:
        metrics['database'] = {
            'patients': Patient.objects.count(),
            'owners': Owner.objects.count(),
            'medical_records': MedicalRecord.objects.count(),
            'vaccinations': Vaccination.objects.count(),
            'prescriptions': Prescription.objects.count(),
            'payments': Payment.objects.count(),
        }
    except Exception as e:
        metrics['database'] = {'error': str(e)}
    
    return Response(metrics)