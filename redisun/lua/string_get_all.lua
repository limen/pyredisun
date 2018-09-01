local vs = {}
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    local v=redis.call('GET',k)
    local ttl=nil
    if ARGV[1]=='1' then
      if ARGV[2]=='EX' then
        ttl=redis.call('TTL',k)
      else
        ttl=redis.call('PTTL',k)
      end
      vs[#vs+1] = {k,v,ttl}
    else
      vs[#vs+1] = {k,v}
    end
  end
end
return vs