local ks={}
for i,v in ipairs(KEYS) do
  if redis.call('EXISTS',v)==1 then
    ks[#ks+1]=v
  end
end
if #ks>0 then
  local k=ks[math.random(#ks)]
  local v=redis.call('GET',k) 
  if ARGV[1]=='1' then
    return {k,v,redis.call('TTL',k)}
  else
    return {k,v}
  end
end
return nil
