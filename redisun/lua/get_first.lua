for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    local v=redis.call('GET',k) 
    if ARGV[1]=='1' then
      return {k,v,redis.call('TTL',k)}
    else
      return {k,v}
    end
  end
end
return nil
