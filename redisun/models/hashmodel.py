from redisun import querybuilder
from redisun.models.vectormodel import VectorModel
from redisun.indexawarelist import IndexAwareList
from redisun.utils import *

_SCRIPT_GET_FIELDS = '_GET_FIELDS_'
_SCRIPT_SET_KVS = '_SET_KVS_'


class HashModel(VectorModel):
    
    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(['user', 'name', 'info'], ['name'], ':')
    
    def create(self, value: dict, ttl: int=0):
        """
        Create hashes and modify their ttl(s) if wanted
        :param value: dict
        :param ttl: int|float
        :return: ok keys : list, ok keys value : dict, failed keys status : dict, failed keys hint : dict
        """
        return self._call_create('set', to_string_dict(value), ttl)
    
    def create_xx(self, value: dict, ttl: int=0):
        return self._call_create('setxx', to_string_dict(value), ttl)
    
    def create_nx(self, value: dict, ttl: int=0):
        return self._call_create('setnx', to_string_dict(value), ttl)
    
    def first(self, fields=(), with_ttl: bool=False):
        return self._one('get_first', fields, with_ttl)
    
    def last(self, fields=(), with_ttl: bool=False):
        return self._one('get_last', fields, with_ttl)
    
    def randone(self, fields=(), with_ttl: bool=False):
        return self._one('get_randone', fields, with_ttl)
    
    def _one(self, script_name: str, fields, with_ttl: bool):
        joined_fields = ','.join(wrap_with_single_quote(fields))
        lua = self._load_script(script_name, {_SCRIPT_GET_FIELDS: joined_fields})
        resp = self._call_lua_func(lua, self.keys(),
                                   [1 if len(fields) > 0 else 0, 1 if with_ttl else 0, self._ttl_in])
        return self._parse_get_response(resp, with_ttl, fields)
    
    def all(self, fields=(), with_ttl: bool=False):
        joined_fields = ','.join(wrap_with_single_quote(fields))
        lua = self._load_script('get_all', {_SCRIPT_GET_FIELDS: joined_fields})
        resp = self._invoke_lua_script(lua, self.keys(),
                                       [1 if len(fields) > 0 else 0, 1 if with_ttl else 0, self._ttl_in])
        return self._parse_get_multi_response(resp, with_ttl, fields)
    
    def getset_one(self, value: dict, fields=(), ttl: int=0):
        value = to_string_dict(value)
        joined_fields = ','.join([''] + wrap_with_single_quote(fields) if len(fields) > 0 else fields)
        hmset_args = ','.join(wrap_dict_to_list(value))
        lua = self._load_script('getset_one', {_SCRIPT_GET_FIELDS: joined_fields, _SCRIPT_SET_KVS: hmset_args})
        resp = self._call_lua_func(lua, [self.first_key()], [1 if len(fields) > 0 else 0, self._ttl_in, ttl])
        return self._parse_getset_response(resp, fields)
    
    def getset_all(self, value: dict, fields=(), ttl: int=0):
        value = to_string_dict(value)
        joined_fields = ','.join([''] + wrap_with_single_quote(fields) if len(fields) > 0 else fields)
        hmset_args = ','.join(wrap_dict_to_list(value))
        lua = self._load_script('getset_all',
                                {_SCRIPT_GET_FIELDS: joined_fields, _SCRIPT_SET_KVS: hmset_args})
        resp = self._invoke_lua_script(lua, self.keys(), [1 if len(fields) > 0 else 0, self._ttl_in, ttl])
        return self._parse_getset_multi_response(resp, fields)
        
    def _call_create(self, script_name: str, value: dict, ttl: int):
        argv = []
        argv += [self._ttl_in, ttl]
        arg_order = 2
        argv_str = ''
        for i, k in enumerate(value):
            argv += [k, value[k]]
            argv_str += 'ARGV[%s],ARGV[%s],' % (arg_order + 1, arg_order + 2)
            arg_order += 2
        argv_str = argv_str.rstrip(',')
        lua = self._load_script(script_name, {_SCRIPT_SET_KVS: argv_str})
        kvs = self._invoke_lua_script(lua, self.keys(), argv)
        return self._parse_set_multi_response(kvs)
    
    def _parse_get_response(self, resp, with_ttl, fields):
        """
        Parse eval response from get_first.lua get_last.lua and get_randone.lua
        :param resp: contains key, value[, ttl]
        :param with_ttl: bool
        :param fields:
        :return: key, value, [ttl]
        """
        if resp is not None:
            resp = IndexAwareList(resp)
            value = self._format_value(resp[1], fields)
            return [resp[0], value] if not with_ttl else [resp[0], value, resp[2]]
        return None
    
    def _parse_getset_response(self, resp, fields):
        """
        Parse eval response from getset_one.lua
        :param resp: contains key, status, old value, msg
        :param fields:
        :return: key, status, old value()
        """
        resp = IndexAwareList(resp)
        return [resp[0], resp[1], self._format_value(resp[2], fields)
                if resp[1] == STATUS_OK else resp[2], resp[3]]

    def _parse_get_multi_response(self, resp, with_ttl, fields):
        ok_keys = []
        failed_keys_status = {}
        ok_keys_value = {}
        failed_keys_hint = {}
        for item_bag in resp:
            item_bag = IndexAwareList(item_bag)
            if item_bag[1] == STATUS_OK:
                ok_keys.append(item_bag[0])
                value = self._format_value(item_bag[2], fields)
                ok_keys_value[item_bag[0]] = value if not with_ttl else [value, item_bag[3]]
            else:
                failed_keys_status[item_bag[0]] = item_bag[1]
                failed_keys_hint[item_bag[0]] = item_bag[3]
    
        return [ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint]
    
    def _parse_set_multi_response(self, resp):
        ok_keys = []
        failed_keys_status = {}
        ok_keys_value = {}
        failed_keys_hint = {}
        for item_bag in resp:
            item_bag = IndexAwareList(item_bag)
            if item_bag[1] == STATUS_OK:
                ok_keys.append(item_bag[0])
                ok_keys_value[item_bag[0]] = self._format_value(item_bag[2])
            else:
                failed_keys_status[item_bag[0]] = item_bag[1]
                failed_keys_hint[item_bag[0]] = item_bag[2]

        return [ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint]
    
    def _parse_getset_multi_response(self, resp, fields):
        ok_keys = []
        failed_keys_status = {}
        ok_kvs = {}
        failed_keys_hint = {}
        for item_bag in resp:
            item_bag = IndexAwareList(item_bag)
            if item_bag[1] == STATUS_OK:
                ok_keys.append(item_bag[0])
                hash_dic = self._format_value(item_bag[2], fields)
                ok_kvs[item_bag[0]] = hash_dic
            else:
                failed_keys_status[item_bag[0]] = item_bag[1]
                failed_keys_hint[item_bag[0]] = item_bag[4]

        return [ok_keys, ok_kvs, failed_keys_status, failed_keys_hint]
    
    def _format_value(self, item, fields=()):
        if item is None:
            return None
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
    
    def _load_script(self, command, replacements=None):
        # To avoid lua script compiling error
        if _SCRIPT_GET_FIELDS in replacements and replacements[_SCRIPT_GET_FIELDS] == '':
            replacements[_SCRIPT_GET_FIELDS] = '0'
        return load_lua_script('hash', command, replacements)
