from redis import StrictRedis

from redisun import querybuilder
from redisun.utils import *

class Model(object):
    """ Manipulate keys of string type
    """
    def __init__(self):
        self._init_query_builder()
        self._init_redis_client()

    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(('greeting','name','date'), ('name','date'), ':')

    def _init_redis_client(self):
        self._redis = StrictRedis(decode_responses=True)

    def xset(self,value, ttl=0, ttl_in_sec=True):
        """ Set multi keys
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        - ttl_in_sec True to set ttl in second, False to set ttl in millisecond
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        keys = self._query_builder.keys()
        lua = load_lua_script('set')
        func = self._redis.register_script(lua)
        values = func(keys=keys, args=[value,'EX' if ttl_in_sec else 'PX',ttl])
        return self._parse_list_to_dict(values)

    def xdel(self):
        """ Delete multi keys
        Return:
        int The number of keys that been deleted successfully
        """
        keys = self.keys()
        if len(keys) > 0:
            return self._redis.delete(*keys)
        return 0

    def set_xx(self,value,ttl=0,ttl_in_sec=True):
        """ Set the key only if it already exists
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        - ttl_in_sec True to set ttl in second, False to set ttl in millisecond
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        keys = self.keys()
        lua = load_lua_script('setx')
        func = self._redis.register_script(lua)
        values = func(keys=keys, args=[value,'EX' if ttl_in_sec else 'PX',ttl,'XX'])
        return self._parse_list_to_dict(values)

    def set_nx(self,value,ttl=0,ttl_in_sec=True):
        """ Set the key only if it does not already exist
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        - ttl_in_sec True to set ttl in second, False to set ttl in millisecond
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        keys = self.keys()
        lua = load_lua_script('setx')
        func = self._redis.register_script(lua)
        values = func(keys=keys, args=[value,'EX' if ttl_in_sec else 'PX',ttl,'NX'])
        return self._parse_list_to_dict(values)

    def update(self, value, ttl=0, ttl_in_sec=True):
        """ Update the key
        alias to setxx
        """
        return self.setxx(value, ttl, ttl_in_sec)

    def getset_one(self, value, ttl=0, ttl_in_sec=True):
        """ Get one key and set new value
        Parameters:
        - value <str>
        - ttl <int>
        - ttl_in_sec <bool>
        Return:
        str|None
        """
        key = self.first_key()
        lua = load_lua_script('getset_one')
        func = self._redis.register_script(lua)
        return func(keys=[key], args=[value,ttl,'EX' if ttl_in_sec else 'PX'])

    def getset_all(self, value, ttl=0, ttl_in_sec=True):
        """ Get multi keys and set new value
        Parameters:
        - value <str>
        - ttl <int>
        - ttl_in_sec <bool>
        Retuen:
        dict {k1:v1,k2:v2,...}
        """
        keys = self.keys()
        lua = load_lua_script('getset_all')
        func = self._redis.register_script(lua)
        values = func(keys=keys, args=[value,ttl,'EX' if ttl_in_sec else 'PX'])
        return self._parse_list_to_dict(values)

    def first(self, with_ttl=False):
        """ Get first existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        keys = self.keys()
        func = self._redis.register_script(load_lua_script('get_first'))
        return func(keys=keys, args=[1 if with_ttl else 0])

    def last(self, with_ttl=False):
        """ Get last existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        keys = self.keys()
        func = self._redis.register_script(load_lua_script('get_last'))
        return func(keys=keys, args=[1 if with_ttl else 0])

    def randone(self, with_ttl=False):
        """ Pick one randomly from existed keys
        Return
        None|list [key,value,ttl(if wanted)]
        """
        keys = self.keys()
        func = self._redis.register_script(load_lua_script('get_randone'))
        return func(keys=keys, args=[1 if with_ttl else 0])

    def all(self, with_ttl=False):
        """ Get all existed keys
        Return:
        dict {k1:[v1,ttl1],k2:[v2,ttl2],...} when with_ttl=True
        dict {k1:v1,k2:v2,...} when with_ttl=False
        """
        keys = self.keys()
        func = self._redis.register_script(load_lua_script('get_all'))
        items = func(keys=keys, args=[1 if with_ttl else 0])
        return self._parse_list_to_dict(items)

    def where(self,field,value):
        self._query_builder.where(field,value)
        return self

    def keys(self):
        return self._query_builder.keys()

    def first_key(self):
        return self._query_builder.first_key()

    def where_in(self,field,values):
        self._query_builder.where_in(field,values)
        return self

    def get_query_builder(self):
        return self._query_builder

    def get_key_field(self,key,field):
        return self._query_builder.get_field(key,field)

    def _call(self, *argv):
        return getattr(self._redis, self._command)(self.first_key(),*argv)

    def _parse_list_to_dict(self,items):
        dic = {}
        for v in items:
            dic[v[0]] = ([v[1],v[2]] if len(v)==3 else v[1])
        return dic

    def __getattr__(self,name):
        self._command = name
        return self._call

if __name__ == '__main__':
    m = Model()
    print(dir(m._query_builder))
