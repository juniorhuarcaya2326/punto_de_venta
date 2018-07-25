from .models import *
from rest_framework import routers, serializers, viewsets


class HotKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotKeys
        fields = '__all__'


class AccionesSerializer(serializers.ModelSerializer):
    hotkeys = HotKeysSerializer()

    class Meta:
        model = Acciones
        fields = '__all__'


class ComponentsSerializer(serializers.ModelSerializer):
    acciones = AccionesSerializer()

    class Meta:
        model = Components
        fields = '__all__'
