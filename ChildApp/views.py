from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db.models import Q
import json
from anam_backend_main import mypermissions
from .models import Child, SiblingGroup, Food, MenuItem, ChildDailyInformation, Picture
from .serializers import ChildSerializer, PictureSerializer, FoodSerializer, MenuItemSerializer, AddFoodSerializer
from .serializers import ChildDailyInformationWriteSerializer, ChildDailyInformationReadSerializer
from anam_backend_main.constants import Admin, Parent, Teacher
from NotificationApp import utils as notfication_utils
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
                if user.role == Teacher:
                    clssnameList = json.loads(user.classnames)
                    query = Q(nameOfClass=clssnameList[0])
                    for classname in clssnameList:
                        query = query | Q(nameOfClass=classname)
                    print(Child.objects.filter(query))
                    return Child.objects.filter(query)
                if user.role == Parent:
                    return user.child.sibling_group.childs
            except Exception:
                return Child.objects.none()

    @action(detail=True, methods=['post'])
    def remove_from_sibling(self, request, pk=None):
        child = self.get_object()
        prev_group_id = child.sibling_group.id
        sibling_group = SiblingGroup.objects.filter(numberOfSiblings=0).first()
        if not sibling_group:
            sibling_group = SiblingGroup()
            sibling_group.save()
        sibling_group.numberOfSiblings -= 1
        sibling_group.save()

        child.sibling_group = sibling_group
        child.save()
        notfication_utils.change_parent_sibling_group(prev_group_id, child.parent)
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
        child_serializer = ChildSerializer(
            child, context=self.get_serializer_context())
        serializer = PictureSerializer(
            child.pictures, many=True, context=self.get_serializer_context())
        return Response({'child': child_serializer.data, 'pictures': serializer.data})

    @action(detail=True, url_path="latest_dailyinfo")
    def get_latest_dailyinformation(self, request, pk=None):
        child = self.get_object()
        daily_info = ChildDailyInformation.objects.filter(
            child=child).order_by('-updated_at').first()
        serializer = ChildDailyInformationReadSerializer(
            daily_info, context=self.get_serializer_context())
        child_serializer = ChildSerializer(
            child, context=self.get_serializer_context())
        return Response({'dailyInfo': serializer.data, 'child': child_serializer.data})

    @action(detail=False, url_path="children")
    def get_children_loggedin_user(self, request):
        user = request.user
        if user.role == Parent:
            child = user.child
            serializer = ChildSerializer(
                child.sibling_group.childs, many=True, context=self.get_serializer_context())
            return Response(serializer.data)
        return Response([])


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
            prev_group_id = child.sibling_group.id
            child.sibling_group = sibling_group
            child.save()
            notfication_utils.change_parent_sibling_group(prev_group_id, child.parent)
        sibling_group.save()

    return Response('success')


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (permissions.IsAuthenticated,
                          mypermissions.IsAdminRole)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (permissions.IsAuthenticated,
                          mypermissions.IsAdminTeacherRole)
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
            menuItem = queryset.filter(
                dayName=dayName, weekName=weekName).order_by('-created_at').first()
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
            menuItem = queryset.filter(
                dayName=dayName, weekName=weekName).order_by('-created_at').first()
            if not menuItem:
                menuItem = MenuItem(weekName=weekName, dayName=dayName)
                menuItem.save()

            foods = serializer.validated_data.pop('foods')
            menuItem.foods.remove(*foods)
            menuItem.save()
            serializer = self.get_serializer(menuItem)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildDailyInformationViewSet(viewsets.ModelViewSet):
    queryset = ChildDailyInformation.objects.all()
    serializer_class = ChildDailyInformationWriteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ChildDailyInformationReadSerializer
        else:
            return ChildDailyInformationWriteSerializer


class MyPictureViewSet(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = PictureSerializer
    permission_classes = (permissions.IsAuthenticated,
                          mypermissions.IsParentRole)

    def get_queryset(self):
        user = self.request.user
        children = user.child.sibling_group.childs.all()
        q_object = Q()
        for child in children:
            q_object = q_object | Q(receiver=child)
        print(Picture.objects.filter(q_object).order_by('-created_at').all())
        return Picture.objects.filter(q_object).order_by('-created_at')
