from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.response import Response
from anam_backend_main import mypermissions
from anam_backend_main.constants import Classroom, All, Admin
import datetime
from .models import SchoolDocument, MiniClub, ExchangeLibrary
from .serializers import UploadSerializer, SchoolDocumentUploadSerializer, SchoolDocumentSerializer,\
                        MiniClubSerializer, ExchangeLibrarySerializer

# Create your views here.


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def uploadPicture(request):

    serializer = UploadSerializer(request.POST, request.FILES)
    if serializer.is_valid():
        url = write_uploaded_file(request.FILES['file'])
        return Response(url)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def write_uploaded_file(f):
    media_root = settings.MEDIA_ROOT
    datestr = datetime.datetime.today().strftime("%d-%m-%y-%H-%M-%S")

    with open(f'{media_root}/pictures/{datestr}{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f"{settings.MEDIA_URL}pictures/{datestr}{f.name}"


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, mypermissions.IsAdminRole))
def uploadSchoolDocument(request, documentFor=All):
    serializer = SchoolDocumentUploadSerializer(data=request.data)
    if serializer.is_valid():
        f = request.FILES['url']
        serializer.save(name=f.name, documentfor=documentFor)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolDocumentViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin):
    queryset = SchoolDocument.objects.all()
    serializer_class = SchoolDocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destory(self, request, *args, **kwargs):
        if request.user.role != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)


class MiniClubViewSet(viewsets.ModelViewSet):
    queryset = MiniClub.objects.all()
    serializer_class = MiniClubSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destory(self, request, *args, **kwargs):
        if request.user.role != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)


class ExchangeLibraryViewSet(viewsets.ModelViewSet):
    queryset = ExchangeLibrary.objects.all()
    serializer_class = ExchangeLibrarySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destory(self, request, *args, **kwargs):
        if request.user.role != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)
