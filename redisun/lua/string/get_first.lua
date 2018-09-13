for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k) == 1 and redis.call('TYPE',k)['ok'] == 'string' then
    local v=redis.call('GET',k)
    local ttl
    if ARGV[1] == '1' then
      if ARGV[2] == 'EX' then
        ttl=redis.call('TTL',k)
      else
        ttl=redis.call('PTTL',k)
      end
    end
    return { k,v,ttl }
  end
end
return nil
