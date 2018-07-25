from rest_framework import serializers
from .models import Producto
from .models import (
    SucursalMensaje, Medico, Cliente, MensajeBody, Vademecum,
    Proforma, Lote, Categoria, VademecumImagen, Promocion,
    VademecumComposicion, PromocionImagen, StockOtherStation,
)


class ProductoSerializer(serializers.ModelSerializer):
    cpi = serializers.FloatField()

    class Meta:
        model = Producto
        fields = ('prod_codigo', 'prod_descorta', 'prod_descripcion', 'proest_descripcion', 'prod_stock_cantidad', 'prod_stock_fraccion',
                  'prec_vta_final', 'prec_vta_sugerido', 'lab_descripcion', 'lab_descorta', 'procodbar_codigo', 'priact_descripcion',
                    'pat_nombres', 'prod_afecto', 'tiprec_descorta', 'tiprec_descripcion', 'cpi')


class ProductoAllSerializer(serializers.ModelSerializer):
    complementarios = ProductoSerializer(many=True, read_only=True)
    similares = ProductoSerializer(many=True, read_only=True)
    cpi = serializers.FloatField()

    class Meta:
        model = Producto
        fields = ('prod_codigo', 'prod_descorta', 'prod_descripcion', 'proest_descripcion', 'prod_stock_cantidad', 'prod_stock_fraccion',
                  'prec_vta_final', 'prec_vta_sugerido', 'lab_descripcion', 'lab_descorta', 'procodbar_codigo', 'priact_descripcion',
                    'pat_nombres', 'prod_afecto', 'similares', 'complementarios', 'tiprec_descorta', 'tiprec_descripcion', 'cpi'
                  )


class ProductoStockSerializer(serializers.ModelSerializer):
    prod_stock_cantidad = serializers.IntegerField()
    prod_stock_fraccion = serializers.FloatField()
    prod_stock_cant_comprometido = serializers.IntegerField()
    prod_stock_fracc_comprometido = serializers.FloatField()
    prod_stock_cant_fisica = serializers.IntegerField()
    prod_stock_fracc_fisico = serializers.FloatField()

    class Meta:
        model = Producto
        fields = ('prod_codigo', 'prod_stock_cantidad',
                  'prod_stock_fraccion', 'prod_stock_cant_comprometido',
                  'prod_stock_fracc_comprometido', 'prod_stock_cant_fisica',
                  'prod_stock_fracc_fisico')


class SucursalMensajeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SucursalMensaje
        fields = '__all__'


class MensajeBodySerializer(serializers.ModelSerializer):

    class Meta:
        model = MensajeBody
        exclude = ('id', 'sumepr_inicia', 'sumepr_finaliza',)


class MedicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medico
        exclude = ('aud_user', 'aud_fecha',)


class ClienteNaturalJuridicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        exclude = ('id',)


class VademecumComposicionSerializer(serializers.ModelSerializer):

    class Meta:
        model = VademecumComposicion
        exclude = ('id',)


class VademecumImagenSerializer(serializers.ModelSerializer):

    class Meta:
        model = VademecumImagen
        fields = ('proima_ruta_url',)


class VademecumSerializer(serializers.ModelSerializer):

    vademecum_imagen = VademecumImagenSerializer(many=True, read_only=True)
    vademecum_composicion = VademecumComposicionSerializer(many=True, read_only=True)

    class Meta:
        model = Vademecum
        fields = ('prod_descripcion', 'pcrsc_descripcion', 'prviad_descripcion',
                  'prod_indicaciones', 'prod_dosificacion',
                  'prod_contraindicaciones', 'prod_reacciones_adversas',
                  'lab_descripcion', 'vademecum_imagen', 'vademecum_composicion',)


class ProformaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proforma
        exclude = ('id', 'estado_proforma',)


class LoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lote
        fields = ('prod_codigo', 'sasl_lote', 'sasl_vencimiento',
            'sasl_cantidad', 'sasl_fraccion', 'sasle_codigo', 'regsan_codigo',
                  'sasle_descripcion')


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        exclude = ('id',)


class PromocionImagenSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromocionImagen
        fields = ('proima_ruta_url', )


class PromocionSerializer(serializers.ModelSerializer):

    promocion_imagen = PromocionImagenSerializer(many=True, read_only=True)

    class Meta:
        model = Promocion
        fields = ('prom_descripcion', 'prom_codigo', 'promocion_imagen',)


class StockOtherStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockOtherStation
        exclude = ('id', )
