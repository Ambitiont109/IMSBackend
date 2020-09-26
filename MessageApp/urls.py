from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'MessageApp'

router = DefaultRouter()
router.register('', views.MessageViewSet, basename='child')

urlpatterns = [
    path('', include(router.urls)),
    path('file/upload/', views.AttachFileUploadView.as_view()),
]
