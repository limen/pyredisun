from redisun import querybuilder
from redisun.models.model import Model
from redisun.indexawarelist import IndexAwareList
from redisun.utils import *


class StringModel(Model):
    """ Manipulate keys of string type
    """
    
    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(['greeting', 'name', 'date'], ['name', 'date'], ':')
    
    def create(self, value, ttl: int=0):
        return self._create('set', value, ttl)
    
    def create_xx(self, value, ttl: int=0):
        return self._create('setxx', value, ttl)
    
    def create_nx(self, value, ttl: int=0):
        return self._create('setnx', value, ttl)
    
    def _create(self, command, value, ttl):
        lua = self._load_script(command)
        resp = self._invoke_lua_script(lua, self.keys(), [to_string(value), self._ttl_in, ttl])
        return self._parse_set_multi_response(resp)
    
    def update(self, value: str, ttl: int=0):
        """
        Alias to create_xx
        """
        return self.create_xx(value, ttl)
    
    def getset_one(self, value: str, ttl: int=0):
        """ Get one key and set new value
        Parameters:
        - value <str>
        - ttl <int>
        Return:
        str|None
        """
        lua = self._load_script('getset_one')
        resp = self._call_lua_func(lua, [self.first_key()], [value, self._ttl_in, ttl])
        return self._parse_getset_response(resp)
    
    def getset_all(self, value, ttl: int=0, with_ttl: bool=False):
        """ Get multi keys and set new value
        Parameters:
        - value <str>
        - ttl <int>
        Retuen:
        dict {k1:v1,k2:v2,...}
        """
        lua = self._load_script('getset_all')
        resp = self._invoke_lua_script(lua, self.keys(), [to_string(value), self._ttl_in, ttl])
        return self._parse_getset_multi_response(resp, with_ttl)
    
    def first(self, with_ttl: bool=False):
        """ Get first existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = self._load_script('get_first')
        resp = self._call_lua_func(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
        return self._parse_get_response(resp, with_ttl)
    
    def last(self, with_ttl: bool=False):
        """ Get last existed key
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = self._load_script('get_last')
        resp = self._call_lua_func(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
        return self._parse_get_response(resp, with_ttl)
    
    def randone(self, with_ttl: bool=False):
        """ Pick one randomly from existed keys
        Return
        None|list [key,value,ttl(if wanted)]
        """
        lua = self._load_script('get_randone')
        resp = self._call_lua_func(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
        return self._parse_get_response(resp, with_ttl)
    
    def all(self, with_ttl: bool=False):
        """ Get all existed keys
        Return:
        dict {k1:[v1,ttl1],k2:[v2,ttl2],...} when with_ttl=True
        dict {k1:v1,k2:v2,...} when with_ttl=False
        """
        lua = self._load_script('get_all')
        resp = self._invoke_lua_script(lua, self.keys(), [1 if with_ttl else 0, self._ttl_in])
        return self._parse_get_multi_response(resp, with_ttl)
    
    def _parse_get_response(self, resp, with_ttl):
        if resp is None:
            return None
        resp = IndexAwareList(resp)
        return [resp[0], self._format_value(resp[1]), resp[2]] if with_ttl \
            else [resp[0], self._format_value(resp[1])]
    
    def _parse_get_multi_response(self, resp, with_ttl):
        """
        Parse get_all.lua response
        :param resp: contains key, status, value[, ttl]
        :return: key, status, value, ttl
        """
        ok_keys = []
        failed_keys_status = {}
        ok_keys_value = {}
        failed_keys_hint = {}
        for item_bag in resp:
            item_bag = IndexAwareList(item_bag)
            if item_bag[1] == STATUS_OK:
                ok_keys.append(item_bag[0])
                value = self._format_value(item_bag[2])
                ok_keys_value[item_bag[0]] = [value, item_bag[3]] if with_ttl else value
            else:
                failed_keys_status[item_bag[0]] = item_bag[1]

        return [ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint]
    
    def _parse_set_response(self, resp):
        pass
    
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
                failed_keys_hint[item_bag[0]] = self._format_value(item_bag[2])

        return [ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint]
    
    def _parse_getset_response(self, resp):
        resp = IndexAwareList(resp)
        return [resp[0], resp[1],
                self._format_value(resp[2]) if resp[1] == STATUS_OK else resp[2], self._format_value(resp[3])]
    
    def _parse_getset_multi_response(self, resp, with_ttl):
        ok_keys = []
        failed_keys_status = {}
        ok_keys_value = {}
        failed_keys_hint = {}
        for item_bag in resp:
            item_bag = IndexAwareList(item_bag)
            if item_bag[1] == STATUS_OK:
                ok_keys.append(item_bag[0])
                value = self._format_value(item_bag[2])
                ok_keys_value[item_bag[0]] = [value, item_bag[3]] if with_ttl else value
            else:
                failed_keys_status[item_bag[0]] = item_bag[1]
                failed_keys_hint[item_bag[0]] = self._format_value(item_bag[4])

        return [ok_keys, ok_keys_value, failed_keys_status, failed_keys_hint]
    
    def _format_value(self, value):
        return value
    
    def _load_script(self, command, replacements=None):
        return load_lua_script('string', command, replacements)
