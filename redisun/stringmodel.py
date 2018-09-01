from redis import StrictRedis

from redisun import querybuilder
from redisun.utils import *

class StringModel(object):
    """ Manipulate keys of string type
    """
    def __init__(self):
        self._init_query_builder()
        self._init_redis_client()
        self._init_ttl_in()

    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(['greeting','name','date'], ['name','date'], ':')

    def _init_redis_client(self):
        self._redis = StrictRedis(decode_responses=True)

    def _init_ttl_in(self):
        self._ttl_in = TTL_IN_SECOND

    def create(self,value, ttl=0):
        """ Set multi keys
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        lua = load_lua_script('string_set')
        return self._invoke_lua_script(lua,self.keys(),[value, self._ttl_in, ttl])

    def remove(self):
        """ Delete multi keys
        Return:
        int The number of keys that been deleted successfully
        """
        keys = self.keys()
        if len(keys) > 0:
            return self._redis.delete(*keys)
        return 0

    def create_xx(self,value,ttl=0):
        """ Set the key only if it already exists
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        lua = load_lua_script('string_setx')
        return self._invoke_lua_script(lua, self.keys(), [value, self._ttl_in, ttl, 'XX'])

    def create_nx(self,value,ttl=0):
        """ Set the key only if it does not already exist
        parameters
        - ttl 0 to keep original ttl, >0 to set new ttl
        Return
        dict {k1:<set rs>,k2:<set rs>,...}
        """
        lua = load_lua_script('string_setx')
        return self._invoke_lua_script(lua,self.keys(),[value, self._ttl_in, ttl, 'NX'])

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
        func = self._redis.register_script(lua)
        return func(keys=[self.first_key()], args=[value,ttl, self._ttl_in])

    def getset_all(self, value, ttl=0):
        """ Get multi keys and set new value
        Parameters:
        - value <str>
        - ttl <int>
        Retuen:
        dict {k1:v1,k2:v2,...}
        """
        lua = load_lua_script('string_getset_all')
        return self._invoke_lua_script(lua,self.keys(),[value,ttl, self._ttl_in])

    def first(self, with_ttl=False):
        """ Get first existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = load_lua_script('string_get_first')
        return self._call_lua_func(lua,self.keys(),[1 if with_ttl else 0, self._ttl_in])

    def last(self, with_ttl=False):
        """ Get last existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = load_lua_script('string_get_last')
        return self._call_lua_func(lua,self.keys(),[1 if with_ttl else 0, self._ttl_in])

    def randone(self, with_ttl=False):
        """ Pick one randomly from existed keys
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = load_lua_script('string_get_randone')
        return self._call_lua_func(lua,self.keys(),[1 if with_ttl else 0, self._ttl_in])

    def all(self, with_ttl=False):
        """ Get all existed keys
        Return:
        dict {k1:[v1,ttl1],k2:[v2,ttl2],...} when with_ttl=True
        dict {k1:v1,k2:v2,...} when with_ttl=False
        """
        lua = load_lua_script('string_get_all')
        return self._invoke_lua_script(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])

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

    def _invoke_lua_script(self,script,keys,args,*argv):
        values = self._call_lua_func(script,keys, args)
        return self._parse_lua_return(values,*argv)

    def _call_lua_func(self,script,keys,args):
        func = self._redis.register_script(script)
        return func(keys=keys, args=args)

    def _parse_lua_return(self,items,*argv):
        dic = {}
        for v in items:
            v = [str(x) if isinstance(x,unicode) else x for x in v]
            item = self._format_item(v[1],*argv)
            dic[v[0]] = ([item, v[2]] if len(v)==3 else item)
        return dic

    def _format_item(self,item,*argv):
        return item

    def __getattr__(self,name):
        self._command = name
        return self._call

if __name__ == '__main__':
    m = Model()
    m.where('name','alice').where('date','09-01').create('alicee')
    print(dir(m._query_builder))
