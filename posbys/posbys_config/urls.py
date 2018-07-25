from .views import *
from django.conf.urls import url
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'components', ComponentesViewSet)
router.register(r'acciones', AccionesViewSet)
router.register(r'hotkeys', HotKeysViewSet)
