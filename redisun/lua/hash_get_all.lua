local vs = {}
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    local v=nil
    if ARGV[1]=='1' then
      v=redis.call('HMGET',k%s)
    else
      v=redis.call('HGETALL',k)
    end
    if ARGV[2]=='1' then
      vs[#vs+1] = {k,v,redis.call('TTL',k)}
    else
      vs[#vs+1] = {k,v}
    end
  end
end
return vs
