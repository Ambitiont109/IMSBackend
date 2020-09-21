from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views
from . import views

app_name = 'UserApp'

router = DefaultRouter()
router.register('', views.UserViewSet, basename='user')

urlpatterns = [
    path('login/', token_views.obtain_auth_token),
    path('', include(router.urls)),

]
