for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    local v=redis.call('GET',k) 
    local ttl
    if ARGV[1]=='1' then
      if ARGV[2]=='EX' then
        ttl=redis.call('TTL',k)
      else
        ttl=redis.call('PTTL',k)
      end
      return {k,v,ttl}
    else
      return {k,v}
    end
  end
end
return nil
