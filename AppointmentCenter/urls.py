from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'AppointmentCenter'

router = DefaultRouter()
router.register('preset_record', views.PresetRecordViewSet, basename='presetRecords')
router.register('preset_appointments', views.PresetAppointmentViewSet, basename='presetAppointments')
router.register('', views.AppointmentViewSet, basename='appointments')


urlpatterns = [
    path('', include(router.urls))

]
