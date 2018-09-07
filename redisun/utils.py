import os

TTL_IN_SECOND = 'EX'
TTL_IN_MILLISECOND = 'PX'

_lua_path = os.path.dirname(__file__) + '/lua'


def load_lua_script(command, replacements=()):
    with open('%s/%s.lua' % (_lua_path, command)) as f:
        return f.read() % replacements if len(replacements) > 0 else f.read()
    
    
def wrap_with_single_quote(fields):
    return ['\'' + f + '\'' for f in fields]


def expand_dict_to_list(dic):
    args = []
    for k in dic:
        args += [k, str(dic[k])]
    return args


def wrap_dict_to_list(dic):
    return wrap_with_single_quote(expand_dict_to_list(dic))


def parse_hash_get_all(ls):
    pass


def parse_hash_multi_get(ls, fields):
    pass


def parse_hash_get(ls, fields):
    dic = {}
    i = 0
    if len(fields) > 0:
        for f in fields:
            dic[f] = ls[i]
            i += 1
    else:
        while i < len(ls):
            dic[ls[i]] = ls[i + 1]
            i += 2
    return dic


def format_bytes(value):
    pass


def parse_batch_getset_return(kvs):
    ok_keys = []
    failed_keys = []
    ok_kvs = {}
    failed_kvs = {}
    for k in kvs:
        if kvs[k][2] == 'OK':
            ok_keys.append(k)
            ok_kvs[k] = kvs[k][1]
        else:
            failed_keys.append(k)
            failed_kvs[k] = kvs[k][1]
    
    return [ok_keys, ok_kvs, failed_keys, failed_kvs]


def parse_single_getset_return(kvs):
    return [kvs[0], kvs[1], True if kvs[2] == 'OK' else False]


def parse_batch_set_return(kvs):
    ok_keys = []
    failed_keys = []
    ok_kvs = {}
    failed_kvs = {}
    for k in kvs:
        if kvs[k][1] == 'OK':
            ok_keys.append(k)
            ok_kvs[k] = kvs[k][1]
        else:
            failed_keys.append(k)
            failed_kvs[k] = kvs[k][1]
    
    return [ok_keys, ok_kvs, failed_keys, failed_kvs]


def parse_lua_batch_return(items):
    dic = {}
    for v in items:
        dic[v.pop(0)] = v
    return dic

