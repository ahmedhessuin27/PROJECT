from django.urls import path
from . import views
from .views import create_service
from .views import delete_service
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('get_service/', views.get_all_services,name='services'),
    path('create_service/', create_service, name='create-service'),
    path('delete_service/<int:service_id>/', delete_service, name='delete-service'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# في urls.py

