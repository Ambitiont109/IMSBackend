from rest_framework import viewsets, mixins, status
from .models import Child
from .serializers import ChildSerializer
from rest_framework import permissions
from django.db.models import Q
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
