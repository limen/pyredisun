from redisun import querybuilder
from redisun.model import Model
from redisun.utils import *


class HashModel(Model):
    
    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(['user', 'name', 'info'], ['name'], ':')
    
    def create(self, value: dict, ttl: int=0):
        """ Create an hash
        Parameters:
        - value <dict>
        """
        return self._call_create('hash_set', value, ttl)
    
    def create_xx(self, value: dict, ttl: int=0):
        return self._call_create('hash_setxx', value, ttl)
    
    def create_nx(self, value: dict, ttl: int=0):
        return self._call_create('hash_setnx', value, ttl)
    
    def first(self, fields=(), with_ttl: bool=False):
        return self._one('hash_get_first', fields, with_ttl)
    
    def last(self, fields=(), with_ttl: bool=False):
        return self._one('hash_get_last', fields, with_ttl)
    
    def randone(self, fields=(), with_ttl: bool=False):
        return self._one('hash_get_randone', fields, with_ttl)
    
    def _one(self, script_name: str, fields, with_ttl: bool):
        joined_fields = ','.join([''] + wrap_with_single_quote(fields) if len(fields) > 0 else fields)
        lua = load_lua_script(script_name, (joined_fields,))
        kvs = self._invoke_lua_script(lua, self.keys(),
                                      [1 if len(fields) > 0 else 0, 1 if with_ttl else 0, self._ttl_in], fields)
        for k in kvs:
            return [k] + (kvs[k] if isinstance(kvs[k], list) else [kvs[k]])
        return None
    
    def all(self, fields, with_ttl: bool=False):
        """ Get hashes
        Parameters:
        - fields <list> the fields you want
        """
        joined_fields = ','.join([''] + wrap_with_single_quote(fields) if len(fields) > 0 else fields)
        lua = load_lua_script('hash_get_all', (joined_fields,))
        return self._invoke_lua_script(lua, self.keys(),
                                       [1 if len(fields) > 0 else 0, 1 if with_ttl else 0, self._ttl_in], fields)
    
    def getset_one(self, value: dict, fields, ttl: int=0):
        joined_fields = ','.join([''] + wrap_with_single_quote(fields) if len(fields) > 0 else fields)
        hmset_args = ','.join(wrap_dict_to_list(value))
        lua = load_lua_script('hash_getset_one', (joined_fields, hmset_args))
        kv = self._invoke_lua_script(lua, [self.first_key()], [1 if len(fields) > 0 else 0, ttl, self._ttl_in], fields)
        return kv.get(self.first_key())
    
    def getset_all(self, value: dict, fields, ttl: int=0):
        joined_fields = ','.join([''] + wrap_with_single_quote(fields) if len(fields) > 0 else fields)
        hmset_args = ','.join(wrap_dict_to_list(value))
        lua = load_lua_script('hash_getset_all', (joined_fields, hmset_args))
        return self._invoke_lua_script(lua, self.keys(), [1 if len(fields) > 0 else 0, ttl, self._ttl_in], fields)
    
    def _call_create(self, script_name: str, value: dict, ttl: int):
        argv = []
        argv += [ttl, self._ttl_in]
        arg_order = 2
        argv_str = ''
        for i, k in enumerate(value):
            argv += [k, value[k]]
            argv_str += 'ARGV[%s],ARGV[%s],' % (arg_order + 1, arg_order + 2)
            arg_order += 2
        argv_str = argv_str.rstrip(',')
        lua = load_lua_script(script_name, (argv_str,))
        return self._invoke_lua_script(lua, self.keys(), argv)
    
    def _format_item(self, item, fields=()):
        if isinstance(item, bytes):
            return item.decode('utf-8')
        elif not isinstance(item, list):
            return item
        item = [x.decode('utf8') if isinstance(x, bytes) else x for x in item]
        dic = {}
        i = 0
        if len(fields) > 0:
            for f in fields:
                dic[f] = item[i]
                i += 1
        else:
            while i < len(item):
                dic[item[i]] = item[i + 1]
                i += 2
        return dic
