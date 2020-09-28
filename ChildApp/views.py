from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db.models import Q
import json
from anam_backend_main import mypermissions
from .models import Child, SiblingGroup, Food, MenuItem
from .serializers import ChildSerializer, PictureSerializer, FoodSerializer, MenuItemSerializer, AddFoodSerializer
from anam_backend_main.constants import Admin
# Create your views here.


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ['nameOfClass']

    def get_queryset(self):
        if(self.request.user.role == Admin):
            return Child.objects.all()
        else:
            user = self.request.user
            try:
                clssnameList = json.loads(user.classnames)
                query = Q(nameOfClass=clssnameList[0])
                print(clssnameList)
                for classname in clssnameList:
                    query = query | Q(nameOfClass=classname)
                return Child.objects.filter(query)
            except Exception:
                return Child.objects.none()

    @action(detail=True, methods=['post'])
    def remove_from_sibling(self, request, pk=None):
        child = self.get_object()
        sibling_group = SiblingGroup.objects.filter(numberOfSiblings=0).first()
        if not sibling_group:
            sibling_group = SiblingGroup()
            sibling_group.save()
        sibling_group.numberOfSiblings += 1
        sibling_group.save()
        child.sibling_group = sibling_group
        child.save()
        return Response(sibling_group.pk)

    @action(detail=True, methods=['post'])
    def upload_picture(self, request, pk=None):
        child = self.get_object()
        print(request.data)

        serializer = PictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(receiver=child)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def pictures(self, request, pk=None):
        child = self.get_object()
        child_serializer = ChildSerializer(child, context=self.get_serializer_context())
        serializer = PictureSerializer(child.pictures, many=True, context=self.get_serializer_context())
        return Response({'child': child_serializer.data, 'pictures': serializer.data})


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def add_child_to_sibling_group(request, pk):
    print(request.user.role)
    if request.user.role != Admin:
        return Response({'userrole': ['You are not Admin']}, status=status.HTTP_400_BAD_REQUEST)
    sibling_group = get_object_or_404(SiblingGroup.objects.all(), pk=pk)
    if 'children' in request.data:
        childIdList = request.data['children']
        children = []
        for child_id in childIdList:
            child = get_object_or_404(Child.objects.all(), pk=child_id)
            children.append(child)
        for child in children:
            if(child.sibling_group.id != sibling_group.id):
                sibling_group.numberOfSiblings += 1
            child.sibling_group = sibling_group
            child.save()
        sibling_group.save()
    return Response('success')


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (permissions.IsAuthenticated, mypermissions.IsAdminRole)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (permissions.IsAuthenticated, mypermissions.IsAdminTeacherRole)
    filterset_fields = ['weekName', 'dayName']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if 'weekName' in request.GET and 'dayName' in request.GET:
            weekName = request.GET.get('weekName')
            dayName = request.GET.get('dayName')
            if not queryset.first():
                menuItem = MenuItem(weekName=weekName, dayName=dayName)
                menuItem.save()
                serializer = self.get_serializer(menuItem)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path="AddFood")
    def addFood(self, request):
        serializer = AddFoodSerializer(data=request.data)
        if serializer.is_valid():
            weekName = serializer.validated_data.pop('weekName')
            dayName = serializer.validated_data.pop('dayName')
            queryset = self.get_queryset()
            menuItem = queryset.filter(dayName=dayName, weekName=weekName).order_by('-created_at').first()
            if not menuItem:
                menuItem = MenuItem(weekName=weekName, dayName=dayName)
                menuItem.save()

            foods = serializer.validated_data.pop('foods')
            menuItem.foods.add(*foods)
            menuItem.save()
            serializer = self.get_serializer(menuItem)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path="removefoodfrommenu")
    def removeFood(self, request):
        serializer = AddFoodSerializer(data=request.data)
        if serializer.is_valid():
            weekName = serializer.validated_data.pop('weekName')
            dayName = serializer.validated_data.pop('dayName')
            queryset = self.get_queryset()
            menuItem = queryset.filter(dayName=dayName, weekName=weekName).order_by('-created_at').first()
            if not menuItem:
                menuItem = MenuItem(weekName=weekName, dayName=dayName)
                menuItem.save()

            foods = serializer.validated_data.pop('foods')
            menuItem.foods.remove(*foods)
            menuItem.save()
            serializer = self.get_serializer(menuItem)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
