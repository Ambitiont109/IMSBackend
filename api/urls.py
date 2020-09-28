from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from ChildApp import views as ChildAppViews
app_name = 'API'

router = DefaultRouter()
router.register(r'schooldocuments', views.SchoolDocumentViewSet, basename='schooldocuments')
router.register(r'foods', ChildAppViews.FoodViewSet, basename='foods'),
router.register(r'menuitems', ChildAppViews.MenuItemViewSet, basename='menuitems')
urlpatterns = [
    path('', include(router.urls)),
    path('user/', include('UserApp.urls')),
    path('child/', include('ChildApp.urls')),
    path('messages/', include('MessageApp.urls')),
    path('appointments/', include('AppointmentCenter.urls')),
    path('uploadpicture/', views.uploadPicture),
    path('upload/document/<slug:documentFor>/', views.uploadSchoolDocument)
]
