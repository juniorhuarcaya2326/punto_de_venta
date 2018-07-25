from django.contrib import admin
from .models import Components,Acciones,HotKeys
# Register your models here.
@admin.register(Components)
class AdminComponents(admin.ModelAdmin):
    pass

@admin.register(Acciones)
class AccionesComponents(admin.ModelAdmin):
    pass

@admin.register(HotKeys)
class HotKeysComponents(admin.ModelAdmin):
    pass