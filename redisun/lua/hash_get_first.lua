for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    local v
    local vr
    if ARGV[1]=='1' then
      v=redis.call('HMGET',k%s)
    else
      v=redis.call('HGETALL',k)
    end
    if ARGV[2]=='1' then
      if ARGV[3]=='EX' then
        vr={k,v,redis.call('TTL',k)}
      else
        vr={k,v,redis.call('PTTL',k)}
      end
    else
      vr={k,v}
    end
    return vr
  end
end
return nil
