local vs={}
for i,k in ipairs(KEYS) do
  local v
  local ttl
  if redis.call('EXISTS',k) == 1 then
    local tp=redis.call('TYPE',k)['ok']
    if tp == 'hash' then
      if ARGV[1] == '1' then
        v=redis.call('HMGET',k,_GET_FIELDS_)
      else
        v=redis.call('HGETALL',k)
      end
      if ARGV[2] == '1' then
        if ARGV[3] == 'EX' then
          ttl=redis.call('TTL',k)
        else
          ttl=redis.call('PTTL',k)
        end
      end
    end
    if tp == 'hash' or tp == 'none' then
      vs[i]={ k,0,v,ttl }
    else
      vs[i]={ k,1,v,ttl }
    end
  else
    vs[i]={ k,3,v,ttl }
  end
end
return vs
