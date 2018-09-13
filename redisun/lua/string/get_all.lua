local vs={}
for i,k in ipairs(KEYS) do
  local tp=redis.call('TYPE',k)['ok']
  local v
  local st
  local ttl
  if tp == 'string' then
    v=redis.call('GET',k)
    if ARGV[1] == '1' then
      if ARGV[2] == 'EX' then
        ttl=redis.call('TTL',k)
      else
        ttl=redis.call('PTTL',k)
      end
    end
    st=0
  elseif tp == 'none' then
    st=0
  else
    st=1
  end
  vs[i]={ k,st,v,ttl }
end
return vs
