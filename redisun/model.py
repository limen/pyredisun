from redis import StrictRedis

from redisun import querybuilder
from redisun.utils import *


class Model(object):
    """ Base model class
    """
    
    def __init__(self):
        self._init_query_builder()
        self._init_redis_client()
        self._init_ttl_in()
    
    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder()
    
    def _init_redis_client(self):
        self._redis = StrictRedis(decode_responses=True)
    
    def _init_ttl_in(self):
        self._ttl_in = TTL_IN_SECOND
    
    def remove(self):
        """ Delete multi keys
        Return:
        int The number of keys that been deleted successfully
        """
        keys = self.keys()
        if len(keys) > 0:
            return self._redis.delete(*keys)
        return 0
    
    def where(self, field, value):
        self._query_builder.where(field, value)
        return self
    
    def keys(self):
        return self._query_builder.keys()
    
    def first_key(self):
        return self._query_builder.first_key()
    
    def where_in(self, field, values):
        self._query_builder.where_in(field, values)
        return self
    
    def get_query_builder(self):
        return self._query_builder
    
    def get_key_field(self, key, field):
        return self._query_builder.get_field(key, field)
    
    def _call(self, *argv):
        return getattr(self._redis, self._command)(self.first_key(), *argv)
    
    def _invoke_lua_script(self, script, keys, args):
        values = self._call_lua_func(script, keys, args)
        return parse_lua_batch_return(values)
    
    def _call_lua_func(self, script, keys, args):
        func = self._redis.register_script(script)
        return func(keys=keys, args=args)
    
    def _format_item(self, item, *argv):
        return item
    
    def __getattr__(self, name):
        self._command = name
        return self._call
