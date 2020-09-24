from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'API'

router = DefaultRouter()
router.register(r'schooldocuments', views.SchoolDocumentViewSet, basename='schooldocuments')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', include('UserApp.urls')),
    path('child/', include('ChildApp.urls')),
    path('uploadpicture/', views.uploadPicture),
    path('upload/document/<slug:documentFor>/', views.uploadSchoolDocument)
]
