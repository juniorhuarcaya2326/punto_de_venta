"""
Definition of api.
"""
import requests
import datetime
import json

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import (
    Medico, Cliente, MensajeBody, Vademecum, Proforma,
    Categoria, Promocion, StockOtherStation
)
from .models import Producto, Lote
from .serializers import (
    ProductoAllSerializer, ProductoSerializer, ProductoStockSerializer, MedicoSerializer,
    ClienteNaturalJuridicoSerializer, MensajeBodySerializer, VademecumSerializer, ProformaSerializer, LoteSerializer,
    CategoriaSerializer, PromocionSerializer, StockOtherStationSerializer,
)
from .services import SolrService


class VademecumViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Vademecum.objects.vademecum_for_pk(pk)
        serializer_class = VademecumSerializer(queryset, many=True)
        return Response(serializer_class.data[0])


class ClienteViewSet(viewsets.ViewSet):

    parser_classes = (JSONParser,)

    def list(self, request, *args, **kwargs):
        query = request.GET.get('query')
        data = SolrService().get_clientes(searched_word=query)
        return Response(data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Cliente.objects.cliente_like_parameters(pk)
        serializer = ClienteNaturalJuridicoSerializer(queryset, many=True)
        return Response(serializer.data[0])

    def create(self, request, *args, **kwargs):
        return Response("cliente creado")

    def update(self, request, pk=None, *args, **kwargs):
        return Response("cliente actualizado")


class MedicoViewSet(viewsets.ViewSet):

    parser_classes = (JSONParser,)

    def list(self, request, *args, **kwargs):

        query = request.GET.get('query')
        data = SolrService.get_medicos(searched_word=query)
        return Response(data)

    def retrieve(self, request, pk=None, *args, **kwargs):

        queryset = Medico.objects.medico_like_parameters(pk)
        serializer_class = MedicoSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def create(self, request, *args, **kwargs):
        return Response("medico creado")

    def update(self, request, pk=None, *args, **kwargs):
        return Response("medico actualizado")


class MensajeViewSet(viewsets.ViewSet):

    parser_classes = (JSONParser,)

    def list(self, request, *args, **kwargs):
        queryset = MensajeBody.objects.mensage_all()
        serializer_class = MensajeBodySerializer(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, pk=None, *args, **kwargs):
        pass


class ProductoViewset(viewsets.ModelViewSet):

    @list_route(methods=['get'], url_path='buscar')
    def get_buscar(self, request, *args, **kwargs):
        q = self.request.GET.get('q')
        print(q)
        q = q.replace('"', '')
        print(q)
        data = SolrService.get_products(searched_word=q)
        return Response(data)

    @list_route(methods=['get'], url_path='similares/(?P<prod_codigo>[0-9]+)')
    def get_similares(self, request, *args, **kwargs):
        prod_codigo = self.kwargs.get('prod_codigo')
        page = 15
        queryset = Producto.objects.get_similares(prod_codigo=prod_codigo, page=page)
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='complementarios/(?P<prod_codigo>[0-9]+)')
    def get_complementarios(self, request, *args, **kwargs):
        prod_codigo = self.kwargs.get('prod_codigo')
        page = 15
        queryset = Producto.objects.get_complementarios(prod_codigo=prod_codigo, page=page)
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='stock/(?P<prod_codigo>[0-9]+)')
    def get_stock(self, request, *args, **kwargs):
        prod_codigo = self.kwargs.get('prod_codigo')
        queryset = Producto.objects.get_stock(prod_codigo=prod_codigo)
        serializer = ProductoStockSerializer(queryset, many=True)
        if len(serializer.data) > 0:
            return Response(serializer.data[0])
        else:
            raise NotFound()

    @list_route(methods=['get'], url_path='barcode/(?P<procodbar_codigo>[A-Za-z0-9]+)')
    def get_barcode(self, request, *args, **kwargs):
        procodbar_codigo = self.kwargs.get('procodbar_codigo')
        queryset = Producto.objects.get_producto_barcode(procodbar_codigo=procodbar_codigo)
        serializer = ProductoAllSerializer(queryset, many=True)
        return Response(serializer.data[0])

    @list_route(methods=['get'], url_path='(?P<prod_codigo>[0-9]+)/lote')
    def mostrar(self, request, prod_codigo, *args, **kwargs):
        queryset = Lote.objects.from_producto(prod_codigo)
        serializer = LoteSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductoBarcodeViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        procodbar_codigo = self.kwargs.get('procodbar_codigo')
        return Producto.objects.get_producto_barcode(procodbar_codigo=procodbar_codigo)


class ProformaLastteViewSet(viewsets.ViewSet):

    parser_classes = (JSONParser,)

    def list(self, request, *args, **kwargs):
        queryset = Proforma.objects.ultima_proforma()
        if not queryset:
            now = datetime.datetime.now()
            new_nro_control = str(now.year)+"-"+str(now.month)+"-1"
            queryset = {new_nro_control: new_nro_control}
            return Response(queryset[0])
        else:
            serializer_class = ProformaSerializer(queryset, many=True)
            return Response(serializer_class.data[0])


class LoteViewSet(viewsets.ModelViewSet):
    serializer_class = LoteSerializer

    def get_queryset(self):
        pass

    @list_route(methods=['get'], url_path='lote/(?P<prod_codigo>[0-9]+)')
    def get_similares(self, request, *args, **kwargs):
        prod_codigo = self.kwargs.get('prod_codigo')
        queryset = Lote.objects.from_producto(prod_codigo=prod_codigo)
        serializer = LoteSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ViewSet):

    parser_classes = (JSONParser,)

    def list(self, request, *args, **kwargs):
        queryset = Categoria.objects.categoria_all()
        serializer_class = CategoriaSerializer(queryset, many=True)
        return Response(serializer_class.data)


from django.core.paginator import Paginator


class PromocionViewSet(viewsets.ModelViewSet):

    serializer_class = PromocionSerializer

    @list_route(methods=['get'], url_path='promo/(?P<cod_cat>[0-9]+)/(?P<params_prod>[A-Za-z0-9-%]+)/(?P<nro_pag>[0-9]+)/(?P<cant_pag>[0-9]+)')
    def get_promocion(self, request, *args, **kwargs):
        cod_cate = self.kwargs.get('cod_cat')
        params_prod = self.kwargs.get('params_prod')
        nro_pag = self.kwargs.get('nro_pag')
        cant_pag = self.kwargs.get('cant_pag')


        if cod_cate == '0' and params_prod == '%':
            queryset = Promocion.objects.all_promocion_with_limit()
            cantidad_registros = len(queryset)
            paginator = Paginator(queryset, cant_pag)
            promocion_details = paginator.page(nro_pag)
            serializer = PromocionSerializer(promocion_details, many=True)
            new_serializer = {}
            new_serializer = {
                'cantidad_registros': cantidad_registros,
                'nro_pagina': nro_pag,
                'cant_pag': cant_pag,
                'data': serializer.data,
            }
        else:
            queryset = Promocion.objects.promocion_with_params(cod_cate, params_prod)
            cantidad_registros = len(queryset)
            paginator = Paginator(queryset, cant_pag)
            promocion_details = paginator.page(nro_pag)
            serializer = PromocionSerializer(promocion_details, many=True)

            new_serializer = {}
            new_serializer = {
                'cantidad_registros': cantidad_registros,
                'nro_pagina': nro_pag,
                'cant_pag': cant_pag,
                'data': serializer.data,
            }
        return Response(new_serializer)


class StockOtherStationViewSet(viewsets.ModelViewSet):

    @list_route(methods=['get'], url_path='stock_other_station/(?P<cod_prod>[0-9]+)')
    def stock_other_station(self, request, *args, **kwargs):
        cod_prod = self.kwargs.get('cod_prod')
        queryset = Producto.objects.get_if_verifica_producto(cod_prod)
        if not queryset:
            return Response(status=status.HTTP_204_NO_CONTENT, data="No encontro producto coincidencia")
        else:
            # print(queryset[0]['prod_codigo'])
            # r = requests.get('http://api.embed.ly/1/oembed?query='+str(queryset[0]['prod_codigo']))
            r = requests.get('http://www.mocky.io/v2/'+"595d61a71100006703098b78")
            d = r.json()
            t = [{"id": 1,
                  "nom_sucursal": "Jr Cuzco, Surco Norte",
                  "stock": 50,
                  "url_imagen": "assets/test-stock/gps-static.png"},
                 {"id": 2,
                  "nom_sucursal": "Jr Andahauaylas, Surco Sur",
                  "stock": 20,
                  "url_imagen": "assets/test-stock/gps-static.png"},
                 {"id": 3,
                  "nom_sucursal": "Calle luna",
                  "stock": 60,
                  "url_imagen": "assets/test-stock/gps-static.png"},
                 {"id": 4,
                  "nom_sucursal": "Jr Moquehua",
                  "stock": 30,
                  "url_imagen": "assets/test-stock/gps-static.png"},
                 {"id": 5,
                  "nom_sucursal": "Jr Moquehua",
                  "stock": 150,
                  "url_imagen": "assets/test-stock/gps-static.png"},
                 {"id": 6,
                  "nom_sucursal": "Jr Moquehua",
                  "stock": 28,
                  "url_imagen": "assets/test-stock/gps-static.png"},]
            return Response(t)


class SendStockBysViewSet(viewsets.ModelViewSet):

    @list_route(methods=['post'], url_path='producto')
    def receive_and_send_product(self, request, *args, **kwargs):

        data = request.data

        url = 'http://127.0.0.1:8000/posbys/peticion_stock_bys/test'
        res = requests.post(url, data)
        return Response()

    @list_route(methods=['get'], url_path='test')
    def test(self, request, *args, **kwargs):
        print("llego la informacion")

        # data = request.data
        return Response()










