local vs={}
for i,k in ipairs(KEYS) do
  local v=false
  local ttl=false
  local st=false
  local tp=redis.call('TYPE',k)['ok']
  if tp=='hash' then
    st=0
    if ARGV[1]=='1' then
      v=redis.call('HMGET',k,_GET_FIELDS_)
    else
      v=redis.call('HGETALL',k)
    end
    if ARGV[2]=='1' then
      if ARGV[3]=='EX' then
        ttl=redis.call('TTL',k)
      else
        ttl=redis.call('PTTL',k)
      end
    end
  elseif tp=='none' then
    st=3
  else
    st=1
  end
  vs[i]={ k,st,v,ttl }
end
return vs
