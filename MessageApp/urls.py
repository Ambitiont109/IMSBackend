from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'MessageApp'

router = DefaultRouter()
router.register('', views.MessageViewSet, basename='child')

urlpatterns = [
   path('compose/', views.MessageComposeView.as_view()),
   path('reply/<int:headerpk>/', views.MessageReplyView.as_view()),
   path('file/upload/', views.AttachFileUploadView.as_view()),

   path('', include(router.urls))
]
