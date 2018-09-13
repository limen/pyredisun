import os

TTL_IN_SECOND = 'EX'
TTL_IN_MILLISECOND = 'PX'

STATUS_OK = 0
STATUS_WRONG_COMMAND = 1
STATUS_SERVER_ERROR = 2
STATUS_EXISTENCE_NOT_SATISFIED = 3

_lua_path = os.path.dirname(__file__) + '/lua'


def load_lua_script(key_type, command, replacements=()):
    with open('%s/%s/%s.lua' % (_lua_path, key_type, command)) as f:
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
