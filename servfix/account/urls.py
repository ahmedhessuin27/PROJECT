from django.urls import path , include
from . import views
from rest_framework import routers
from django.conf import settings
from .views import getimage
from django.conf.urls.static import static
router=routers.DefaultRouter()
router.register(r'add_work' , views.ADDwork , basename='add_work')
urlpatterns = [
    path('register/', views.register,name='register'),
    path('userinfo/',views.current_user,name='user_info'),
    path('userinfo/update',views.update_user,name='update_user'),
    path('forgot_password/', views.forgot_password,name='forgot_password'), 
    path('reset_password/<str:token>', views.reset_password,name='reset_password'),
    path('provider_register/', views.provider_register,name='provider_register'),
    path('providerinfo/',views.current_provider,name='provider_info'),
    path('providerinfo/update',views.update_provider,name='update_provider'), 
    path('reviews/<str:pk>', views.create_review,name='create_review'),
    path('all/<str:pk>', views.allprovider,name='allprovider'),
    path('favourite/<str:pro_id>', views.provider_favourite,name='provider_favourite'),
    path('show_all_favourites',views.get_all_favourites,name='show_all_favourites'),
    path('change_password',views.update_password,name='update_password'),
     path('',include(router.urls),name='add_work'),
    path('selec_provider/<str:sele_id>',views.selected_provider, name='selected_provider'),
    path('all_work',getimage.as_view(),name='all_work'),
    path('delete_work/<str:work_id>',views.delete_work,name='delete_work'),
    path('delete_fav/<str:fav_id>',views.delete_favourite,name='delete_favourite'),
    path('get_providers/<str:pk>',views.get_providers_for_service, name='get_providers_for_service'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
