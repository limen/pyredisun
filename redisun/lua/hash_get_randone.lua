local ks={}
for i,v in ipairs(KEYS) do
  if redis.call('EXISTS',v)==1 then
    ks[#ks+1]=v
  end
end
if #ks>0 then
  local k=ks[math.random(#ks)]
  local v=nil
  if ARGV[1]=='1' then
    v=redis.call('HMGET',k%s)
  else
    v=redis.call('HGETALL',k)
  end
  if ARGV[2]=='1' then
    if ARGV[3]=='EX' then
      ttl=redis.call('TTL',k)
    else
      ttl=redis.call('PTTL',k)
    end
    return {{k,v,ttl}}
  else
    return {{k,v}}
  end
end
return {}
