from redis import StrictRedis

from redisun import querybuilder
from redisun.model import Model
from redisun.utils import *


class StringModel(Model):
    """ Manipulate keys of string type
    """
    
    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(['greeting', 'name', 'date'], ['name', 'date'], ':')
    
    def create(self, value, ttl=0):
        """ Set multi keys
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        lua = load_lua_script('string_set')
        return self._invoke_lua_script(lua, self.keys(), [value, self._ttl_in, ttl])
    
    def remove(self):
        """ Delete multi keys
        Return:
        int The number of keys that been deleted successfully
        """
        keys = self.keys()
        if len(keys) > 0:
            return self._redis.delete(*keys)
        return 0
    
    def create_xx(self, value, ttl=0):
        """ Set the key only if it already exists
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        lua = load_lua_script('string_setx')
        return self._invoke_lua_script(lua, self.keys(), [value, self._ttl_in, ttl, 'XX'])
    
    def create_nx(self, value, ttl=0):
        """ Set the key only if it does not already exist
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        lua = load_lua_script('string_setx')
        return self._invoke_lua_script(lua, self.keys(), [value, self._ttl_in, ttl, 'NX'])
    
    def update(self, value, ttl=0):
        """ Update the key
        alias to setxx
        """
        return self.create_xx(value, ttl)
    
    def getset_one(self, value, ttl=0):
        """ Get one key and set new value
        Parameters:
        - value <str>
        - ttl <int>
        Return:
        str|None
        """
        lua = load_lua_script('string_getset_one')
        return self._call_lua_func(lua, [self.first_key()], [value, ttl, self._ttl_in])
    
    def getset_all(self, value, ttl=0):
        """ Get multi keys and set new value
        Parameters:
        - value <str>
        - ttl <int>
        Retuen:
        dict {k1:v1,k2:v2,...}
        """
        lua = load_lua_script('string_getset_all')
        return self._invoke_lua_script(lua, self.keys(), [value, ttl, self._ttl_in])
    
    def first(self, with_ttl=False):
        """ Get first existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = load_lua_script('string_get_first')
        return self._call_lua_func(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
    
    def last(self, with_ttl=False):
        """ Get last existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = load_lua_script('string_get_last')
        return self._call_lua_func(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
    
    def randone(self, with_ttl=False):
        """ Pick one randomly from existed keys
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = load_lua_script('string_get_randone')
        return self._call_lua_func(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
    
    def all(self, with_ttl=False):
        """ Get all existed keys
        Return:
        dict {k1:[v1,ttl1],k2:[v2,ttl2],...} when with_ttl=True
        dict {k1:v1,k2:v2,...} when with_ttl=False
        """
        lua = load_lua_script('string_get_all')
        return self._invoke_lua_script(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
