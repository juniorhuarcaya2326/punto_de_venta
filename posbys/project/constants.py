from enum import Enum


class ProductoTipo(Enum):
    PRINCIPAL = "parentDocument"
    SIMILAR = "similar"
    COMPLEMENTARIO = "complementario"


class SolrServiceCore(Enum):
    PRODUCTO_CORE = "productocore"
    MEDICO_CORE = "medicocore"
