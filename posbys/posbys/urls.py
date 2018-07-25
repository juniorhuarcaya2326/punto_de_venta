"""
Definition of urls for posbys.
"""

from rest_framework.routers import DefaultRouter
from .api import (
    ProductoViewset, MensajeViewSet,MedicoViewSet,
    ClienteViewSet, VademecumViewSet,
    ProductoBarcodeViewSet, ProformaLastteViewSet,
    LoteViewSet, CategoriaViewSet,
    PromocionViewSet, StockOtherStationViewSet,
    SendStockBysViewSet
)

router = DefaultRouter()
#/producto/buscar?q=<query>&page=<pag>
router.register(r'producto', ProductoViewset, 'producto')
#127.0.0.1:8000/posbys/producto/similares/2/?page=15
#router.register(r'producto/similares/(?P<prod_codigo>[1-9]+)', ProductoSimilarViewSet, 'similar')
#127.0.0.1:8000/posbys/producto/complementarios/2/?page=15
#router.register(r'producto/complementarios/(?P<prod_codigo>[1-9]+)', ProductoComplementarioViewSet, 'complementario')
#127.0.0.1:8000/posbys/producto/stock/4
#router.register(r'producto/stock/(?P<prod_codigo>[1-9]+)', ProductoStockViewSet, 'stock')
#127.0.0.1:8000/posbys/producto/barcode/pr123
#router.register(r'producto/barcode/(?P<procodbar_codigo>[A-Za-z0-9]+)', ProductoBarcodeViewSet, 'barcode')

#/producto/complementarios/<prod_codigo>/?page=<pagina>
router.register(r'mensaje', MensajeViewSet, 'mensaje')
router.register(r'medico', MedicoViewSet, 'medico')
router.register(r'cliente', ClienteViewSet, 'cliente')
router.register(r'vademecum', VademecumViewSet, 'vademecum')

router.register(r'proforma_last', ProformaLastteViewSet, 'proforma_last')
router.register(r'categoria', CategoriaViewSet, 'categoria')
router.register(r'promocion', PromocionViewSet, 'promocion')
router.register(r'peticion_stock_bys', SendStockBysViewSet, 'peticion_stock_bys')
router.register(r'peticion_stock_bys', SendStockBysViewSet, 'peticion_stock_bys')

router.register('lote', LoteViewSet, 'lote')

router.register('stock', StockOtherStationViewSet, 'stock')

urlpatterns = router.urls
