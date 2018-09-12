import os

TTL_IN_SECOND = 'EX'
TTL_IN_MILLISECOND = 'PX'

STATUS_OK = 0
STATUS_WRONG_COMMAND = 1
STATUS_SERVER_ERROR = 2
STATUS_EXISTENCE_NOT_SATISFIED = 3

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


def parse_string_getset_return(kvs):
    return kvs


def parse_string_batch_getset_return(kvs, with_ttl: bool):
    ok_keys = []
    failed_keys_status = {}
    ok_kvs = {}
    failed_keys_hint = {}
    for kv in kvs:
        if kv[1] == STATUS_OK:
            ok_keys.append(kv[0])
            ok_kvs[kv[0]] = [kv[2], kv[3]] if with_ttl else kv[2]
        else:
            failed_keys_status[kv[0]] = kv[1]
            failed_keys_hint[kv[0]] = kv[4]

    return [ok_keys, ok_kvs, failed_keys_status, failed_keys_hint]


def parse_string_batch_get_return(kvs, with_ttl: bool):
    ok_keys = []
    failed_keys_status = {}
    ok_kvs = {}
    for kv in kvs:
        if kv[1] == STATUS_OK:
            ok_keys.append(kv[0])
            ok_kvs[kv[0]] = [kv[2], kv[3]] if with_ttl else kv[2]
        else:
            failed_keys_status[kv[0]] = kv[1]
    
    return [ok_keys, ok_kvs, failed_keys_status]


# HASH getset
def parse_hash_getset_return(kvs, fields=()):
    return [kvs[0], kvs[1], parse_hash_get(kvs[2], fields) if kvs[1] == STATUS_OK else None]


# HASH batch getset
def parse_hash_batch_getset_return(kvs, with_ttl: bool, fields=()):
    ok_keys = []
    failed_keys_status = {}
    ok_kvs = {}
    failed_keys_hint = {}
    for kv in kvs:
        if kv[1] == STATUS_OK:
            ok_keys.append(kv[0])
            hash_dic = parse_hash_get(kv[2], fields)
            ok_kvs[kv[0]] = [hash_dic, kv[3]] if with_ttl else hash_dic
        else:
            failed_keys_status[kv[0]] = kv[1]
            failed_keys_hint[kv[0]] = kv[4]
    
    return [ok_keys, ok_kvs, failed_keys_status, failed_keys_hint]


def parse_hash_batch_get_return(kvs, with_ttl: bool, fields=()):
    ok_keys = []
    failed_keys_status = {}
    ok_kvs = {}
    for kv in kvs:
        if kv[1] == STATUS_OK:
            ok_keys.append(kv[0])
            hash_dic = parse_hash_get(kv[2], fields)
            ok_kvs[kv[0]] = [hash_dic, kv[3]] if with_ttl else hash_dic
        else:
            failed_keys_status[kv[0]] = kv[1]
    
    return [ok_keys, ok_kvs, failed_keys_status]


def parse_batch_set_return(kvs):
    ok_keys = []
    failed_keys = []
    ok_kvs = {}
    failed_kvs = {}
    for kv in kvs:
        if kv[1] == STATUS_OK:
            ok_keys.append(kv[0])
            ok_kvs[kv[0]] = kv[2]
        else:
            failed_keys.append(kv[0])
            failed_kvs[kv[0]] = kv[2]
    
    return [ok_keys, ok_kvs, failed_keys, failed_kvs]

