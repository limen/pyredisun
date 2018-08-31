import os

TTL_IN_SECOND = 'EX'
TTL_IN_MILLISECOND = 'PX' 

_lua_path = os.path.dirname(__file__) + '/lua'

def load_lua_script(command,replacements=()):
    with open('%s/%s.lua' % (_lua_path,command)) as f:
        return f.read() % replacements if len(replacements)>0 else f.read()
