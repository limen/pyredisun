local lk
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    lk=k
  end
end
if lk~=nil then
  local v=redis.call('GET',lk) 
  if ARGV[1]=='1' then
    if ARGV[2]=='EX' then
      ttl=redis.call('TTL',lk)
    else
      ttl=redis.call('PTTL',lk)
    end
    return {lk,v,ttl}
  else
    return {lk,v}
  end
end
return nil
