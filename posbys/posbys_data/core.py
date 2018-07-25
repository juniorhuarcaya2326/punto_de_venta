
import warnings
from collections import deque
from django.db import connections
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.pool import _ConnectionRecord as _ConnectionRecordBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .wrapper import Wrapper

import time


__all__ = ['get_engine', 'get_meta', 'get_tables']

Base = declarative_base()

class CacheType(type):

    def __getattribute__(cls, name):
        if name == 'models':
            warnings.warn('Cache.models attribute is deprecated. '
                          'Use Cache.sa_models instead.',
                          DeprecationWarning, stacklevel=2)
        return type.__getattribute__(cls, name)


class Cache(object):
    """Module level cache"""
    __metaclass__ = CacheType
    engines = {}


SQLALCHEMY_ENGINES = {
    'mysql': 'mysql',
    'postgresql': 'postgresql',
    'postgresql_psycopg2': 'postgresql+psycopg2',
    'oracle': 'oracle',
}
SQLALCHEMY_ENGINES.update(getattr(settings, 'ALDJEMY_ENGINES', {}))


def get_engine_string(alias):
    sett = connections[alias].settings_dict
    return sett['ENGINE'].rsplit('.')[-1]


def get_connection_string(alias='default'):
    engine = SQLALCHEMY_ENGINES[get_engine_string(alias)]
    options = '?charset=utf8' if engine == 'mysql' else ''
    return engine + '://' + options


def get_engine(alias='default'):
    if alias not in Cache.engines:
        engine_string = get_engine_string(alias)
        # we have to use autocommit=True, because SQLAlchemy
        # is not aware of Django transactions
        kw = {}
        if engine_string == 'sqlite3':
            kw['native_datetime'] = True

        pool = DjangoPool(alias=alias, creator=None)
        Cache.engines[alias] = create_engine(get_connection_string(alias),
                                             pool=pool, **kw)
    return Cache.engines[alias]


def get_session(alias='default'):
    # create a configured "Session" class
    Session = sessionmaker(bind=get_engine(alias=alias))

    # create a Session
    return Session()

def get_meta():
    if not getattr(Cache, 'meta', None):
        Cache.meta = MetaData()
    return Cache.meta



class DjangoPool(NullPool):
    def __init__(self, alias, *args, **kwargs):
        super(DjangoPool, self).__init__(*args, **kwargs)
        self.alias = alias

    def status(self):
        return "DjangoPool"

    def _create_connection(self):
        return _ConnectionRecord(self, self.alias)

    def recreate(self):
        self.logger.info("Pool recreating")

        return DjangoPool(
            self.alias,
            self._creator,
            recycle=self._recycle,
            echo=self.echo,
            logging_name=self._orig_logging_name,
            use_threadlocal=self._use_threadlocal
        )


class _ConnectionRecord(_ConnectionRecordBase):
    def __init__(self, pool, alias):
        self.__pool = pool
        self.info = {}
        self.finalize_callback = deque()
        self.starttime = time.time()

        self.alias = alias
        self.wrap = False
        #pool.dispatch.first_connect.exec_once(self.connection, self)
        pool.dispatch.connect(self.connection, self)
        self.wrap = True

    @property
    def connection(self):
        connection = connections[self.alias]
        if connection.connection is None:
            connection._cursor()        
        if self.wrap:
            return Wrapper(connection.connection)
        return connection.connection

    def close(self):
        pass

    def invalidate(self, e=None, soft=False):
        pass

    def get_connection(self):
        return self.connection