local vs = {}
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    local v=redis.call('GET',k)
    if ARGV[1]=='1' then
      vs[#vs+1] = {k,v,redis.call('TTL',k)}
    else
      vs[#vs+1] = {k,v}
    end
  end
end
return vs
