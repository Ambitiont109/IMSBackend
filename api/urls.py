from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'API'

router = DefaultRouter()
# router.register(r'students', views.StudentViewSet, basename='student')


urlpatterns = [
    path('user/', include('UserApp.urls')),
    path('child/', include('ChildApp.urls')),
    path('uploadpicture/', views.uploadPicture)
]
