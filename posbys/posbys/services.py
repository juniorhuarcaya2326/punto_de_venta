import json
from itertools import filterfalse
from logging import getLogger

import requests
from django.conf import settings

from project.constants import ProductoTipo, SolrServiceCore

logger = getLogger('posbys')


class SolrService(object):
    @classmethod
    def call_service(cls, solr_core, filter_params):
        response = requests.get(
            '%s%s/select' % (settings.BYS_POS_SOLR_URL, solr_core),
            params=filter_params)
        json_data = json.loads(response.text)
        return json_data

    @classmethod
    def get_products(cls, searched_word, start=0, numrows=settings.BYS_POS_SOLR_MAX_DOC_PARENT):
        json_data = {}
        if searched_word != '' and searched_word is not None and searched_word != "":
            # query para el solr

            filter_params = dict()
            filter_params['q'] = searched_by_keyword(searched_word)
            filter_params['fq'] = 'type:%s' % ProductoTipo.PRINCIPAL.value
            filter_params['start'] = start
            filter_params['rows'] = numrows
            filter_params[
                'fl'] = '*,[child parentFilter="type:parentDocument" limit=%s]' % settings.BYS_POS_SOLR_MAX_DOC_CHILD
            filter_params['wt'] = 'json'
            response = None

            try:
                json_data = cls.call_service(solr_core=SolrServiceCore.PRODUCTO_CORE.value, filter_params=filter_params)
                # en caso de que la primera busqueda pueda haber
                # incluido el codigo del producto y haya producido un error
                if 'error' in json_data:
                    # el codigo de busqueda puede ser el codigo de barras
                    logger.info("La busqueda fallo con el codigo de producto, se intentara con el codigo de barras")
                    filter_params['q'] = searched_by_keyword(text=searched_word, usa_codigo_producto=False)
                    json_data = cls.call_service(solr_core=SolrServiceCore.PRODUCTO_CORE.value,
                                                 filter_params=filter_params)

                if 'response' in json_data:
                    productos = json_data['response']['docs']
                    logger.info('Se encontraron %s productos con el texto %s' % (
                        json_data['response']['numFound'], searched_word))

                    productos = map(lambda producto: cls.get_productos_relacionados(producto), productos)
                    return productos
            except Exception as e:
                logger.error("Ocurrio un error al buscar los productos. "
                             "Exception: %s, mensaje: %s, response: %s" % (type(e).__name__, str(e), str(response)))
                json_data['success'] = False
                json_data['message'] = str(e)
        return json_data

    @classmethod
    def get_productos_relacionados(cls, producto):
        if '_childDocuments_' in producto:
            productos_relacionados = producto['_childDocuments_']
            similares = filterfalse(lambda p: p['type'] != ProductoTipo.SIMILAR.value, productos_relacionados)
            complementarios = filterfalse(lambda p: p['type'] != ProductoTipo.COMPLEMENTARIO.value,
                                          productos_relacionados)

            similares = list(similares)
            complementarios = list(complementarios)
            if similares:
                similares = map(lambda p: remove_keys(('type', '_version_',), p), similares)
                producto['similares'] = similares

            if complementarios:
                complementarios = map(lambda p: remove_keys(('type', '_version_',), p), complementarios)
                producto['complementarios'] = complementarios

            remove_keys(('uuid', '_childDocuments_', 'type', '_version_',), producto)
        return producto

    @classmethod
    def get_medicos(cls, searched_word, keyword_fields=('med_codigo', 'med_nombrecompleto'),
                    start=0, numrows=20):
        json_data = {}
        if searched_word != '' and searched_word is not None and searched_word != "":
            data_search_product = list()
            # query para el solr
            data_search_product.append(searched_params(keyword_fields, searched_word, 'med_codigo'))

            filter_params = dict()
            filter_params['q'] = '*:*'
            filter_params['fq'] = data_search_product
            filter_params['start'] = int(start)
            filter_params['rows'] = int(numrows)
            filter_params['wt'] = 'json'

            try:
                response = requests.get('%s%s/select' % (settings.BYS_POS_SOLR_URL, 'medicocore'),

                                        params=filter_params)
                json_data = json.loads(response.text)
                if 'response' in json_data:
                    productos = json_data['response']['docs']
                    return productos
            except Exception as e:
                json_data['success'] = False
                json_data['message'] = str(e)
        return json_data

    def get_clientes(self, searched_word, keyword_fields=('tipdocide_numero', 'clie_nombre_completo'),
                    start=0, numrows=20):
        json_data = {}
        if searched_word != '' and searched_word is not None and searched_word != "":
            data_search_product = list()
            # query para el solr
            data_search_product.append(searched_params(keyword_fields, searched_word))

            filter_params = dict()
            filter_params['q'] = '*:*'
            filter_params['fq'] = data_search_product
            filter_params['start'] = int(start)
            filter_params['rows'] = int(numrows)
            filter_params['wt'] = 'json'

            try:
                response = requests.get('%s%s/select' % (settings.BYS_POS_SOLR_URL, 'clientecore'),

                                        params=filter_params)
                json_data = json.loads(response.text)
                if 'response' in json_data:
                    productos = json_data['response']['docs']

                    #     # TODO implementar nested docs en solr para obtener los similares y complementarios
                    #     for producto in productos:
                    #         self.get_productos_relacionados(producto)
                    #
                    # TODO implementar nested docs en solr para obtener los similares y complementarios
                    #for producto in productos:
                        #self.get_productos_relacionados(producto)

                    return productos
            except Exception as e:
                json_data['success'] = False
                json_data['message'] = str(e)
        return json_data


def searched_params(fields, text, codigo=None):
    if len(text.split()) > 1:
        logger.info(
            "La busqueda de producto no incluye el codigo de producto, el"
            " termino de busqueda es texto y contiene mas de una palabra: %s" % text)

        # termino de busqueda con mas de una palabra: se debe utilizar comilla doble
        # (priact_descripcion:"micolis 1%" OR prod_descorta:"micolis 1%" OR prod_descripcion:"micolis 1%")
        multiple_filters = ['%s:"%s"' % (field, text) for field in fields]
    else:
        # si el termino de busqueda es de una sola palabra: utilizamos el comodin * para la busqueda
        # (prod_descripcion:mico* OR priact_descripcion:mico* OR prod_descorta:mico*)
        multiple_filters = ['%s:%s*' % (field, text) for field in fields]

        try:
            # posibilidad de que el termino sea el codigo del producto
            val = int(text)
            if codigo:
                multiple_filters.append('%s:%s' % codigo, val)
                logger.info('La busqueda de medico incluye el codigo de medico %s' % val)
            else:
                logger.info('La busqueda de medico incluye el codigo de medico')
        except ValueError:
            logger.info(
                'La busqueda de medico no inclucye el codigo de medico, el termino de busqueda es texto: %s' % text)

    return '({items})'.format(items=' OR '.join(multiple_filters))


def searched_by_keyword(text, usa_codigo_producto=True, keyword='keyword'):
    # la busqueda se hace a los campos definidos como keyword en el schema.xml del core

    if len(text.split()) > 1:
        logger.info(
            "La busqueda de producto no incluye el codigo de producto, el termino de busqueda es "
            "texto y contiene mas de una palabra: %s" % text)

        # termino de busqueda con mas de una palabra: se debe utilizar comilla doble 
        _filter = '%s:"%s"' % (keyword, text)
    else:
        # si el termino de busqueda es de una sola palabra: utilizamos el comodin * para la busqueda
        _filter = '%s:%s*' % (keyword, text)
        try:
            # posibilidad de que el termino sea el codigo del producto
            val = int(text)
            if usa_codigo_producto:
                _filter = 'prod_codigo:%s' % val
                logger.info('La busqueda de producto incluye el codigo de producto %s' % val)
            else:
                _filter = 'procodbar_codigo:%s' % val
                logger.info('La busqueda de producto incluye el codigo de barras %s' % val)
        except ValueError:
            logger.info(
                'La busqueda de producto no incluye el codigo de producto, el termino de busqueda es texto: %s' % text)

    return _filter


def remove_keys(keys, item):
    for key in keys:
        item.pop(key, None)
    return item
