from redis import StrictRedis

from redisun import querybuilder
from redisun.model import Model
from redisun.utils import *

class HashModel(Model):

    def _init_query_builder(self):
        self._query_builder = querybuilder.QueryBuilder(['user','name','info'], ['name'], ':')

    def create(self,value,ttl=0):
        """ Create an hash
        Parameters:
        - value <dict>
        """
        return self._call_create('hash_set',value,ttl)

    def create_xx(self,value,ttl=0):
        return self._call_create('hash_setxx',value,ttl)

    def create_nx(self,value,ttl=0):
        return self._call_create('hash_setnx',value,ttl)

    def all(self, fields=[], with_ttl=False):
        """ Get hashes
        Parameters:
        - fields <list> the fields you want
        """
        joined_fields = ','.join([''] + self._wrap_hash_fields(fields) if len(fields)>0 else fields)
        lua = load_lua_script('hash_get_all', (joined_fields,))
        return self._invoke_lua_script(lua, self.keys(), [1 if len(fields)>0 else 0, 1 if with_ttl else 0, self._ttl_in], fields)

    def getset_one(self, value, fields=[], ttl=0):
        joined_fields = ','.join([''] + self._wrap_hash_fields(fields) if len(fields)>0 else fields)
        hmset_args = ','.join(self._wrap_dict_for_hmset(value))
        lua = load_lua_script('hash_getset_one', (joined_fields,hmset_args))
        return self._invoke_lua_script(lua, self.keys(), [1 if len(fields)>0 else 0, ttl, self._ttl_in], fields)

    def _call_create(self,script_name,value,ttl):
        argv = []
        argv += [ttl, self._ttl_in]
        arg_order = 2 
        argv_str = ''
        for i,k in enumerate(value):
            argv += [k, value[k]]
            argv_str += 'ARGV[%s],ARGV[%s],' % (arg_order+1, arg_order+2)
            arg_order += 2
        argv_str = argv_str.rstrip(',')
        lua = load_lua_script(script_name, (argv_str,))
        return self._invoke_lua_script(lua, self.keys(), argv)

    def _format_item(self, item, fields=[]):
        if isinstance(item, str):
            return item
        dic = {}
        i = 0
        if len(fields)>0:
            for f in fields:
                dic[f] = item[i]
                i += 1
        else:
            while i<len(item):
                dic[item[i]] = item[i+1]
                i += 2
        return dic

    def _wrap_hash_fields(self,fields):
        return ['\'' + f + '\'' for f in fields]

    def _wrap_dict_for_hmset(self,value):
        i = 0
        args = []
        for k in value:
            args += ['\'' + k + '\'', '\'' + value[k] + '\'']
        return args

if __name__ == '__main__':
    hm = HashModel()
    rs = hm.where('name','alice').create({'name':'alice','date':'09-01'})
    print(hm.all(['name']))
    print(hm.getset_one({'name':'bob','age':'22'},['name']))
    rs = hm.where('name','alice').create_xx({'name':'alice','date':'09-02'})
    print(hm.all())
    rs = hm.where('name','alice').create_nx({'name':'alice','date':'09-03'})
    print(hm.all())
    print(hm.remove())
