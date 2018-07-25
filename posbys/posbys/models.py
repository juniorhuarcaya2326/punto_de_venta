from django.db import models
from .managers import (
    ProductoManager, MensajeManager, MedicoManager,
    VademecumManager, ClienteNaturalJuridicoManager,
    LoteManager, ProformaManager,
    VademecumImagenManager, CategoriaAllManager,
    PromocionManager, VademecumComposicionManager,
    PromocionImagenManager,
)
from datetime import datetime as dt
import time


class Producto(models.Model):

    prod_codigo = models.IntegerField(primary_key=True)
    prod_descorta = models.CharField(max_length=30)
    prod_descripcion = models.CharField(max_length=100)
    proest_descripcion = models.CharField(max_length=30)
    prod_stock_cantidad = models.PositiveIntegerField()
    prod_stock_fraccion = models.PositiveIntegerField()
    procodbar_codigo = models.CharField(max_length=20)
    prec_vta_final = models.FloatField()
    prec_vta_sugerido = models.FloatField()
    priact_descripcion = models.CharField(max_length=100)
    prod_afecto = models.SmallIntegerField()
    lab_descorta = models.CharField(max_length=10)
    lab_descripcion = models.CharField(max_length=80)
    pat_nombres = models.CharField(max_length=100)
    tiprec_descorta = models.CharField(max_length=10)
    tiprec_descripcion = models.CharField(max_length=100)
    objects = ProductoManager()

    class Meta:
        managed = False

    def __str__(self):
        return self.prod_descripcion

    @property
    def similares(self):
        return Producto.objects.get_similares(prod_codigo=self.prod_codigo, page=4)

    @property
    def complementarios(self):
        return Producto.objects.get_complementarios(prod_codigo=self.prod_codigo, page=4)

    @property
    def cpi(self):
         return 0.5


class Medico(models.Model):
    med_codigo = models.AutoField(primary_key=True)
    colmed_codigo = models.CharField(max_length=3, blank=True, null=True)
    colmed_descripcion = models.CharField(max_length=50, blank=True, null=True)
    med_matricula = models.CharField(max_length=50, blank=True, null=True)
    med_nombrecompleto = models.CharField(max_length=80, blank=True, null=True)
    aud_user = models.CharField(max_length=6, blank=True, null=True)
    aud_fecha = models.DateTimeField(blank=True, null=True)

    objects = MedicoManager()

    class Meta:
        db_table = 'medico'


class MensajeBody(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    time_out = models.CharField(max_length=20, blank=True, null=True)
    sucmen_mensaje = models.CharField(max_length=200, blank=True, null=True)
    sumepr_inicia = models.DateTimeField(blank=True, null=True)
    sumepr_finaliza = models.DateTimeField(blank=True, null=True)
    sumepr_hora_inicio = models.TimeField(blank=True, null=True)
    sumepr_hora_finaliza = models.TimeField(blank=True, null=True)

    objects = MensajeManager()

    def __str__(self):
        return u'{0} - {1}'.format(self.sucmen_mensaje, self.sumepr_hora_inicio, self.sumepr_hora_finaliza)


class SucursalMensaje(models.Model):
    sucmen_anno = models.SmallIntegerField(primary_key=True)
    sucmen_codigo = models.SmallIntegerField()
    activo = models.NullBooleanField()
    sucmen_mensaje = models.CharField(max_length=200, blank=True, null=True)
    aud_user = models.CharField(max_length=6, blank=True, null=True)
    aud_fecha = models.DateTimeField(blank=True, null=True)

    objects = MensajeManager()

    def __str__(self):
        return u'{0} - {1}'.format(self.sucmen_codigo, self.sucmen_mensaje)

    class Meta:
        db_table = 'sucursal_mensaje'
        unique_together = (('sucmen_anno', 'sucmen_codigo'),)


class SucursalMensajePresentacion(models.Model):
    sucmen_anno = models.SmallIntegerField(primary_key=True)
    sucmen_codigo = models.SmallIntegerField()
    sumepr_item = models.SmallIntegerField()
    activo = models.NullBooleanField()
    sumepr_inicia = models.DateField(blank=True, null=True)
    sumepr_finaliza = models.DateField(blank=True, null=True)
    sumepr_hora_inicio = models.TimeField(blank=True, null=True)
    sumepr_hora_finaliza = models.TimeField(blank=True, null=True)
    aud_user = models.CharField(max_length=6, blank=True, null=True)
    aud_fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'sucursal_mensaje_presentacion'
        unique_together = (('sucmen_anno', 'sucmen_codigo', 'sumepr_item'),)


class VademecumComposicion(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    priact_codigo = models.IntegerField()
    priact_descripcion = models.CharField(max_length=100)
    prprac_principal = models.IntegerField()

    objects = VademecumComposicionManager()

    def __str__(self):
        return u'{0} - {1}'.format(self.priact_codigo, self.priact_descripcion)


class VademecumImagen(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    prod_codigo = models.IntegerField()
    proima_ruta_url = models.CharField(max_length=100)

    objects = VademecumImagenManager()

    def __str__(self):
        return u'{0} - {1}'.format(self.prod_codigo, self.proima_ruta_url)


class Vademecum(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    pcrsc_descripcion = models.CharField(max_length=100)
    prviad_descripcion = models.CharField(max_length=30)
    prod_indicaciones = models.CharField(max_length=100)
    prod_dosificacion = models.CharField(max_length=500)
    prod_contraindicaciones = models.CharField(max_length=1000)
    prod_reacciones_adversas = models.CharField(max_length=1000)
    lab_descripcion = models.CharField(max_length=100)
    prod_codigo = models.IntegerField()
    prod_descripcion = models.CharField(max_length=100)

    objects = VademecumManager()

    class Meta:
        managed = False

    def __str__(self):
        return u'{0} - {1}'.format(self.lab_descripcion, self.prod_descripcion)

    @property
    def vademecum_imagen(self):
        return VademecumImagen.objects.get_imagen_for_producto(pro_codigo=self.prod_codigo)

    @property
    def vademecum_composicion(self):
        return VademecumComposicion.objects.Composicion_for_vademecum(prod_codigo=self.prod_codigo)


class Proforma(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    prof_anno = models.SmallIntegerField(default=1)
    nro_control_proforma = models.CharField(max_length=100)
    estado_proforma = models.CharField(max_length=30)

    objects = ProformaManager()

    class Meta:
        db_table = 'proforma'

    def __str__(self):
        return u'{0}'.format(self.nro_control_proforma)


class Lote(models.Model):
    prod_codigo = models.IntegerField(primary_key=True)
    sasl_lote = models.CharField(max_length=20)
    sasl_vencimiento = models.DateField()
    sasl_cantidad = models.PositiveIntegerField()
    sasl_fraccion = models.PositiveIntegerField()
    regsan_codigo = models.IntegerField()
    sasle_codigo = models.SmallIntegerField()
    sasle_descripcion = models.CharField(max_length=50)

    aud_user = models.CharField(max_length=6)
    aud_fecha = models.DateTimeField()

    objects = LoteManager()

    class Meta:
        managed = False
        db_table = 'sucursal_almacen_stock_lote'

    def __str__(self):
        return u'{0}-{1}'.format(self.prod_codigo, self.sasl_lote)

    def __repr__(self):
        return u'{0}-{1}'.format(self.prod_codigo, self.sasl_lote)


class Categoria(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    pcbsc_codigo = models.SmallIntegerField()
    pcbsc_descripcion = models.CharField(max_length=50)

    objects = CategoriaAllManager()

    def __str__(self):
        return u'{0} - {1}'.format(self.pcbsc_codigo, self.pcbsc_descripcion)


class PromocionImagen(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    prom_codigo = models.SmallIntegerField()
    proima_ruta_url = models.CharField(max_length=100)

    objects = PromocionImagenManager()

    def __str__(self):
        return u'{0}'.format(self.proima_ruta_url)


class Promocion(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    prod_codigo = models.IntegerField()
    prom_descripcion = models.CharField(max_length=100)
    prom_codigo = models.SmallIntegerField()

    objects = PromocionManager()

    def __str__(self):
        return u'{0} - {1}'.format(self.prom_codigo, self.prom_descripcion)

    @property
    def promocion_imagen(self):
        return PromocionImagen.objects.imagen_to_promocion(prom_codigo=self.prom_codigo)


class Cliente(models.Model):

    id = models.IntegerField(primary_key=True)
    clie_codigo = models.IntegerField()
    clie_nombre_completo = models.CharField(max_length=100)
    rucnom_razsoc = models.CharField(max_length=100)

    objects = ClienteNaturalJuridicoManager()

    def __str__(self):
        return u'{0} - {1}'.format(self.clie_codigo, self.clie_nombre_completo)


class StockOtherStation(models.Model):

    id = models.IntegerField(primary_key=True)
    nom_sucursal = models.CharField(max_length=100)
    stock = models.IntegerField()
    imagen_sucursal_url = models.CharField(max_length=100)





