from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'NotificationApp'

router = DefaultRouter()
router.register('headers', views.NotificationDataViewSet, basename='notification_headers')
router.register('', views.NotificationRecordListSet, basename='notification')


urlpatterns = [
    path('', include(router.urls)),
]
