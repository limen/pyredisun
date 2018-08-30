import os

_lua_path = os.path.dirname(__file__) + '/lua'

def load_lua_script(command):
    with open('%s/%s.lua' % (_lua_path,command)) as f:
        return f.read()
