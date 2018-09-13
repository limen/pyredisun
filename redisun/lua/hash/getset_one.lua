local ov=false
local st=false
local ms=false
local tp=redis.call('TYPE',KEYS[1])['ok']
if tp == 'hash' then
  if ARGV[1] == '1' then
    ov=redis.call('HMGET',KEYS[1],_GET_FIELDS_)
  else
    ov=redis.call('HGETALL',KEYS[1])
  end
end
if tp == 'hash' or tp == 'none' then
  local lt=tonumber(ARGV[3])
  ms=redis.call('HMSET',KEYS[1],_SET_KVS_)['ok']
  if lt>0 and ms=='OK' then
    if ARGV[2] == 'EX' then
      redis.call('EXPIRE',KEYS[1],lt)
    else
      redis.call('PEXPIRE',KEYS[1],lt)
    end
  end
  if ms=='OK' then
    st=0
  else
    st=2
  end
else
  st=1
end
return { KEYS[1],st,ov,ms }
