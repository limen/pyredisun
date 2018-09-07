Lua script notes

+  Check type of key before operation
+  "set" like commands should return ok keys, failed keys and failed reasons
+  Script should return tuple(s) in pattern {<key>, <op_code>, <value>[, <ttl>]}

Return value explain

+ key: the redis key
+ op code: the status code which tells the operation is ok or failed