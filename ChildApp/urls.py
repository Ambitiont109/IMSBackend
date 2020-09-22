from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views
from . import views

app_name = 'ChildApp'

router = DefaultRouter()
router.register('', views.ChildViewSet, basename='child')

urlpatterns = [
    path('', include(router.urls)),

]
