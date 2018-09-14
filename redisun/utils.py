from os.path import dirname

TTL_IN_SECOND = 'EX'
TTL_IN_MILLISECOND = 'PX'

STATUS_OK = 0
STATUS_WRONG_COMMAND = 1
STATUS_SERVER_ERROR = 2
STATUS_EXISTENCE_NOT_SATISFIED = 3

_lua_path = dirname(__file__) + '/lua'


def load_lua_script(key_type, command, replacements=None):
    with open('%s/%s/%s.lua' % (_lua_path, key_type, command)) as f:
        lua = f.read()
    if replacements is not None:
        for k in replacements:
            lua = lua.replace(k, replacements[k])
    return lua
    
    
def wrap_with_single_quote(fields):
    return ['\'' + f + '\'' for f in fields]


def expand_dict_to_list(dic):
    args = []
    for k in dic:
        args += [k, str(dic[k])]
    return args


def wrap_dict_to_list(dic):
    return wrap_with_single_quote(expand_dict_to_list(dic))


def to_string(value):
    return value if isinstance(value, str) else str(value)


def to_strings(values):
    return [x if isinstance(x, str) else str(x) for x in values]


def to_string_dict(dic):
    string_dic = {}
    for k in dic:
        string_dic[k] = dic[k] if isinstance(dic[k], str) else str(dic[k])
    return string_dic
