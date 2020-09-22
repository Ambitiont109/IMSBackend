from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from django.conf import settings
from .serializers import UploadSerializer
import datetime
from rest_framework.response import Response

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
