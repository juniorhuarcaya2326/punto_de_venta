from rest_framework import viewsets
from .models import *
from .serializer import HotKeysSerializer, ComponentsSerializer, AccionesSerializer


# Create your views here.
class ComponentesViewSet(viewsets.ModelViewSet):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer


class AccionesViewSet(viewsets.ModelViewSet):
    queryset = Acciones.objects.all()
    serializer_class = AccionesSerializer


class HotKeysViewSet(viewsets.ModelViewSet):
    queryset = HotKeys.objects.all()
    serializer_class = HotKeysSerializer
