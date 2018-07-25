"""
Definition of managers.
"""
import datetime
from django.db import models, connection
#from datetime import datetime, timedelta
from datetime import datetime as dt
import time
import string


class ProductoManager(models.Manager):

    def get_complementarios(self, prod_codigo, page=4):

        return self.raw("""
                  SELECT
                    prod_codigo,
                    prod_descorta,
                    prod_descripcion,
                    proest_descripcion,
                    prod_stock_cantidad,
                    prod_stock_fraccion,
                    prec_vta_final,
                    prec_vta_sugerido,
                    lab_descripcion,
                    lab_descorta,
                    procodbar_codigo,
                    priact_descripcion,
                    pat_nombres,
                    prod_afecto,
                    tiprec_descorta,
                    tiprec_descripcion
                  FROM lv_producto_complementario
                  WHERE parent = %s
                  LIMIT %s;
                """, [prod_codigo, page])

    def get_similares(self, prod_codigo, page=4):

        return self.raw("""
                  SELECT
                    prod_codigo,
                    prod_descorta,
                    prod_descripcion,
                    proest_descripcion,
                    prod_stock_cantidad,
                    prod_stock_fraccion,
                    prec_vta_final,
                    prec_vta_sugerido,
                    lab_descripcion,
                    lab_descorta,
                    procodbar_codigo,
                    priact_descripcion,
                    pat_nombres,
                    prod_afecto,
                    tiprec_descorta,
                    tiprec_descripcion
                  FROM lv_producto_similar
                  WHERE parent = %s
                  LIMIT %s;
                """, [prod_codigo, page])

    def get_stock(self, prod_codigo):
        return self.raw("""
            SELECT 
                prod_codigo,
                prod_stock_cantidad,
                prod_stock_fraccion,
                prod_stock_cant_comprometido,
                prod_stock_fracc_comprometido,
                prod_stock_cant_fisica,
                prod_stock_fracc_fisico
            FROM producto
            WHERE prod_codigo = %s;    
        """, [prod_codigo])

    def get_producto_barcode(self, procodbar_codigo):
        return self.raw("""
          SELECT
                    prod_codigo,
                    prod_descorta,
                    prod_descripcion,
                    proest_descripcion,
                    prod_stock_cantidad,
                    prod_stock_fraccion,
                    prec_vta_final,
                    prec_vta_sugerido,
                    lab_descripcion,
                    lab_descorta,
                    procodbar_codigo,
                    priact_descripcion,
                    pat_nombres,
                    prod_afecto,
                    tiprec_descorta,
                    tiprec_descripcion
                  FROM lv_producto
                  WHERE procodbar_codigo = %s;
        """, [procodbar_codigo])

    def get_if_verifica_producto(self, pk):

        with connection.cursor() as cursor:
            params = pk

            cursor.execute('''
                select * from producto where prod_codigo = %s
            ''', [params, ])
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [dict(zip(columns, row)) for row in result]

        return dict_rows


class MensajeManager(models.Manager):

    def mensage_all(self):

        with connection.cursor() as cursor:

            cursor.execute("""
                              select 1 as id,
                              smp.sucmen_codigo,
                              extract(EPOCH from(smp.sumepr_hora_finaliza::time - smp.sumepr_hora_inicio::time)) as time_out,
                              sm.sucmen_mensaje, to_char(smp.sumepr_inicia, 'YYYY-MM-DD') as sumepr_inicia,
                              to_char(smp.sumepr_finaliza, 'YYYY-MM-DD') as sumepr_finaliza,
                              smp.sumepr_hora_inicio,
                              smp.sumepr_hora_finaliza
                              from sucursal_mensaje as sm
                              INNER JOIN sucursal_mensaje_presentacion as smp
                                on sm.sucmen_codigo = smp.sucmen_codigo and sm.sucmen_anno = smp.sucmen_anno
                              where
                                (now()::date >= smp.sumepr_inicia and now()::date <= smp.sumepr_finaliza)
                        """)

            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [dict(zip(columns, row)) for row in result]

        return dict_rows


class VademecumComposicionManager(models.Manager):

    def Composicion_for_vademecum(self, prod_codigo):
        pass


class VademecumManager(models.Manager):

    def vademecum_for_pk(self, pk):
        params = pk

        with connection.cursor() as cursor:

            cursor.execute('''select 1 as id,
                                pro.prod_descripcion,
                                pro.pcrsc_descripcion, pro.prviad_descripcion,
                                pro.prod_indicaciones, pro.prod_dosificacion,
                                pro.prod_contraindicaciones, pro.prod_reacciones_adversas,
                                lab.lab_descripcion, pro.prod_codigo
                                from producto pro, laboratorio lab
                                where pro.prod_codigo = %s
                                and pro.lab_codigo = lab.lab_codigo''', [params, ])

            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [self.model(**dict(zip(columns, row))) for row in result]
        return dict_rows


class VademecumImagenManager(models.Manager):

    def get_imagen_for_producto(self, pro_codigo):

        with connection.cursor() as cursor:

            cursor.execute('''select 1 as id,
                              prod_codigo, proima_ruta_url 
                              from producto_imagen
                              where prod_codigo = %s ''', [
                                                            pro_codigo,
                                                        ])

            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [dict(zip(columns, row)) for row in result]
        return dict_rows


class ProformaManager(models.Manager):

    def ultima_proforma(self):

        with connection.cursor() as cursor:

            cursor.execute('''select 1 as id,
                    concat(to_char( now(), 'YYYY'),'-',to_char( now(), 'MM'),'-', pr.prof_codigo+1) as nro_control_proforma,
                    pr_estado.proest_descripcion,
                    pr_estado.activo as estado_proforma
                    from proforma as pr,
                    proforma_estado as pr_estado
                    WHERE
                    pr_estado.proest_codigo = 2
                    ORDER BY pr.prof_codigo DESC LIMIT 1''')

            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [dict(zip(columns, row)) for row in result]
        return dict_rows


class MedicoManager(models.Manager):

    def medico_all(self, query):
        pass

    def medico_like_parameters(self, query):
        pass

    def medico_insert(self):
        pass

    def medico_update(self):
        pass


class ClienteNaturalJuridicoManager(models.Manager):

    def cliente_all(self, query):
        pass

    def cliente_like_parameters(self, pk):
        pass

    def cliente_insert(self):
        pass

    def cliente_update(self):
        pass


class LoteManager(models.Manager):

    def from_producto(self, prod_codigo):

        with connection.cursor() as cursor:
            cursor.execute('''
            select 
                prod_codigo,
                sasl_lote,
                sasl_vencimiento,
                sasl_cantidad,
                sasl_fraccion,
                regsan_codigo,
                estado.sasle_codigo,
                estado.sasle_descripcion
            from sucursal_almacen_stock_lote as lote
            join sucursal_almacen_stock_lote_estado as estado
              on lote.sasle_codigo = estado.sasle_codigo
            where 
              lote.activo= TRUE 
              and lote.sasle_codigo != 3 -- estado inactivo
              and sasl_vencimiento > now()::date
              and prod_codigo = %s
            order by sasl_vencimiento ASC;
            ''', [prod_codigo, ])

            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()

        dict_rows = [self.model(**dict(zip(columns, row))) for row in result]

        return dict_rows


class CategoriaAllManager(models.Manager):

    def categoria_all(self):

        with connection.cursor() as cursor:

            cursor.execute('''
                          select 1 as id, pcbsc_codigo, pcbsc_descripcion
                          from producto_clasificador_bys
                          ''')

            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [dict(zip(columns, row)) for row in result]

        return dict_rows


class PromocionManager(models.Manager):

    def promocion_with_params(self, cod_cate, params_prod):
        params_cod_cate = cod_cate
        new_params_prod = params_prod
        new_params_prod = "%{0}%".format(new_params_prod)

        with connection.cursor() as cursor:

            cursor.execute('''
            SELECT DISTINCT prom.prom_codigo,
                prom.prom_descripcion as prom_descripcion,
                prom.prom_codigo as prom_codigo
                from (
                  /* RESUMEN TABLA(PROD_CODIGO)*/
                  SELECT
                    pv.prod_codigo as prod_codigo,
                    pv.prom_codigo as prom_codigo
                  FROM promocion_venta AS pv
                  JOIN producto AS p
                  ON pv.prod_codigo = p.prod_codigo
                UNION
                  SELECT
                    pe.prod_codigo as prod_codigo,
                    pe.prom_codigo as prom_codigo
                  FROM promocion_entrega AS pe
                  JOIN producto AS p
                  ON pe.prod_codigo = p.prod_codigo
                ) as resumen
                join producto as prod
                  on resumen.prod_codigo = prod.prod_codigo
                join promocion prom
                  on resumen.prom_codigo = prom.prom_codigo
                left outer join producto_clasificador_bys cat
                  on prod.pcbsc_codigo = cat.pcbsc_codigo
                INNER JOIN laboratorio lab
                  on prod.lab_codigo = lab.lab_codigo
                  where cat.pcbsc_codigo = %s
                  or 
                  ( lab.lab_descripcion similar TO %s or
                    prom.prom_descripcion similar TO %s or
                    CAST(prod.prod_codigo AS TEXT) like %s
                  ) limit 9 offset 0
            ''', [params_cod_cate, new_params_prod, new_params_prod, new_params_prod, ])
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [self.model(**dict(zip(columns, row))) for row in result]
        return dict_rows

    def all_promocion_with_limit(self):

        with connection.cursor() as cursor:

            cursor.execute('''
                select prom_descripcion, 
                prom_codigo  
                from promocion 
                limit 200 OFFSET 0
            ''')
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [self.model(**dict(zip(columns, row))) for row in result]

        return dict_rows


class PromocionImagenManager(models.Manager):

    def imagen_to_promocion(self, prom_codigo):
        params = prom_codigo

        with connection.cursor() as cursor:

            cursor.execute('''
                        select 1 as id,
                        prom_codigo,
                        proima_ruta_url
                        from promocion_imagen
                        where prom_codigo = %s
            ''', [params, ])

            columns = [column[0] for column in cursor.description]
            result = cursor.fetchall()
            dict_rows = [self.model(**dict(zip(columns, row))) for row in result]

        return dict_rows


