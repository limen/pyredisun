from redis import StrictRedis

import querybuilder
from utils import *

class Model(object):
    def __init__(self):
        self._redis = StrictRedis()
        self._init_query_builder()

    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(('greeting','name','date'), ('name','date'), ':')

    def set(self,value, ttl=0, ttl_in_sec=True):
        """ Set the key
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        - ttl_in_sec True to set ttl in second, False to set ttl in millisecond
        """
        keys = self._query_builder.keys()
        lua = load_lua_script('set')
        func = self._redis.register_script(lua)
        return func(keys=keys, args=[value,'EX' if ttl_in_sec else 'PX',ttl])

    def setxx(self,value,ttl=0,ttl_in_sec=True):
        """ Set the key only if it already exists
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        - ttl_in_sec True to set ttl in second, False to set ttl in millisecond
        """
        keys = self._query_builder.keys()
        lua = load_lua_script('setx')
        func = self._redis.register_script(lua)
        return func(keys=keys, args=[value,'EX' if ttl_in_sec else 'PX',ttl,'XX'])

    def setnx(self,value,ttl=0,ttl_in_sec=True):
        """ Set the key only if it does not already exist
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        - ttl_in_sec True to set ttl in second, False to set ttl in millisecond
        """
        keys = self._query_builder.keys()
        lua = load_lua_script('setx')
        func = self._redis.register_script(lua)
        return func(keys=keys, args=[value,'EX' if ttl_in_sec else 'PX',ttl,'NX'])

    def update(self, value, ttl=0, ttl_in_sec=True):
        """ Update the key
        alias to setxx
        """
        return self.setxx(value, ttl, ttl_in_sec)

    def first(self, with_ttl=False):
        key = self._first_key()
        func = self._redis.register_script(load_lua_script('get'))
        values = func(keys=[key], args=[1 if with_ttl else 0])
        return values[0] if len(values)>0 else None

    def last(self, with_ttl=False):
        key = self._last_key()
        func = self._redis.register_script(load_lua_script('get'))
        values = func(keys=[key], args=[1 if with_ttl else 0])
        return values[0] if len(values)>0 else None

    def randone(self, with_ttl=False):
        key = self._random_key()
        func = self._redis.register_script(load_lua_script('get'))
        values = func(keys=[key], args=[1 if with_ttl else 0])
        return values[0] if len(values)>0 else None

    def all(self, with_ttl=False):
        keys = self._keys()
        func = self._redis.register_script(load_lua_script('get'))
        return func(keys=keys, args=[1 if with_ttl else 0])

    def delete(self):
        keys = self._query_builder.keys()
        if len(keys) > 0:
            return self._redis.delete(*keys)
        return 0

    def where(self,field,value):
        self._query_builder.where(field,value)
        return self

    def where_in(self,field,values):
        self._query_builder.where_in(field,values)
        return self

    def get_query_builder(self):
        return self._query_builder

    def getset(self, value, ttl=0, ttl_in_sec=True):
        key = self._first_key()
        lua = load_lua_script('getset')
        func = self._redis.register_script(lua)
        return func(keys=[key], args=[value,ttl,'EX' if ttl_in_sec else 'PX'])

    def _keys(self):
        return self._query_builder.keys()

    def _first_key(self):
        return self._query_builder.first_key()

    def _last_key(self):
        return self._query_builder.last_key()

    def _random_key(self):
        return self._query_builder.random_key()

    def _call(self, *argv):
        return getattr(self._redis, self._command)(self._first_key(),*argv)

    def __getattr__(self,name):
        self._command = name
        return self._call

if __name__ == '__main__':
    m = Model()
    m.where('name','alice').where_in('date',['09-01','09-02'])
#    m.where('name','alice').where_in('date',('09-01','09-02'))
#    m.hmset({'send_at':'09:00','created_at':'08:59'})
#    print(m.hgetall())
#    print(m.hmget('send_at','created_at'))
#    print(m.ttl())
#    print(m.delete())
#    print(m.hmget('send_at','created_at'))
#    print(m.ttl())
    print(m.setxx('1234'))
    print(m.first())
    print(m.first(True))
    print(m.last())
    print(m.last(True))
    print(m.all())
    print(m.all(True))
    print(m.getset('12345', 300))
#    print(m.getset('hello-alice',100))
#    print(m.randone(True))
#    print(m.first(True))
#    print(m.last(True))
