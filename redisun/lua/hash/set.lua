local vs={}
local lt=tonumber(ARGV[2])
for i,k in ipairs(KEYS) do
  local tp=redis.call('TYPE',k)['ok']
  if tp == 'hash' or tp == 'none' then
    local ms=redis.call('HMSET',k,_SET_KVS_)['ok']
    if lt > 0 and ms == 'OK' then
      vs[i]={ k,0,ms }
      if ARGV[1] == 'EX' then
        redis.call('EXPIRE',k,lt)
      else
        redis.call('PEXPIRE',k,lt)
      end
    else
      vs[i]={ k,2,ms }
    end
  else
    vs[i]={ k,1,nil }
  end
end
return vs
