from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from .models import Child, SiblingGroup
from .serializers import ChildSerializer, PictureSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.db.models import Q
from django.http import QueryDict

import json
from anam_backend_main.constants import Parent, Teacher, Admin, \
                                        Bamboo, Iroko, Baobab, Acajou
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
            picture = serializer.save(receiver=child)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
