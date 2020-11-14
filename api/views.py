from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.response import Response
from anam_backend_main import mypermissions
from anam_backend_main.constants import Classroom, All, Admin
import datetime
from .models import SchoolDocument, MiniClub, ExchangeLibrary, BookStatus, Marketing
from .serializers import UploadSerializer, SchoolDocumentUploadSerializer, SchoolDocumentSerializer,\
    MiniClubSerializer, ExchangeLibrarySerializer, MarketingReadSerializer, MarketingWriteSerializer,\
    RegisterChildMiniClubSerializer, UnRegisterChildMiniClubSerializer
from NotificationApp.utils import send_broadcast
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
    queryset = MiniClub.objects.order_by('-date')
    serializer_class = MiniClubSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destory(self, request, *args, **kwargs):
        if request.user.role != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path="thisweek")
    def get_thisweek_club(self, request):
        first_day_of_week = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().isoweekday() % 7)
        clubs = MiniClub.objects.filter(date__gte=first_day_of_week).order_by('date')
        serializer = MiniClubSerializer(
            clubs, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path="unregister")
    def remove_siblings_from_club(self, request, pk=None):
        club = self.get_object()
        serializer = UnRegisterChildMiniClubSerializer(data=request.data)
        if serializer.is_valid():
            child = serializer.validated_data.get('child')
            club.children.remove(*child.sibling_group.childs.all())
            club_serializer = MiniClubSerializer(club, context=self.get_serializer_context())
            return Response(club_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path="register")
    def addChildToClub(self, request, pk=None):
        club = self.get_object()
        serializer = RegisterChildMiniClubSerializer(
            data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            child = serializer.validated_data.get('child')
            children = club.children.all()
            if child not in children:
                club.children.add(child)
                club.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        send_broadcast()
        return response


class ExchangeLibraryViewSet(viewsets.ModelViewSet):
    queryset = ExchangeLibrary.objects.order_by('title').all()
    serializer_class = ExchangeLibrarySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destory(self, request, *args, **kwargs):
        if request.user.role != Admin:
            return Response("You don't have enough permission", status=status.HTTP_400_BAD_REQUEST)
        return super().destory(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path="rentBook")
    def rent_book(self, request, pk=None):
        book = self.get_object()
        if book.status == BookStatus.RENTED:
            return Response("Already Rented By Another User", status=status.HTTP_400_BAD_REQUEST)
        book.status = BookStatus.RENTED
        book.child = request.user.child
        book.save()
        serializer = ExchangeLibrarySerializer(
            book, context=self.get_serializer_context())
        return Response(serializer.data)


class MarketingViewSet(viewsets.ModelViewSet):
    queryset = Marketing.objects.order_by('-created_at').all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MarketingReadSerializer
        else:
            return MarketingWriteSerializer
