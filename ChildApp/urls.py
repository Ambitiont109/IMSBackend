from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ChildApp'

router = DefaultRouter()
router.register('', views.ChildViewSet, basename='child')

urlpatterns = [
    path('sibling/pictures/', views.MyPictureViewSet.as_view()),
    path('sibling/pictures/<int:pk>/', views.MyPictureViewSet.as_view()),
    path('', include(router.urls)),

    path('sibling/<int:pk>/add/', views.add_child_to_sibling_group)
]
