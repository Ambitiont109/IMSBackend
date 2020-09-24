from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status, viewsets, mixins
from django.conf import settings
from .serializers import UploadSerializer, SchoolDocumentUploadSerializer, SchoolDocumentSerializer
import datetime
from rest_framework.response import Response
from anam_backend_main import mypermissions
from anam_backend_main.constants import Classroom, All
from .models import SchoolDocument
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


class SchoolDocumentReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolDocument.objects.all()
    serializer_class = SchoolDocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class SchoolDocumentDestroyViewSet(mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    queryset = SchoolDocument.objects.all()
    permission_classes = (permissions.IsAuthenticated, mypermissions.IsAdminRole)
