local lk=nil
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    lk=k
  end
end
if lk~=nil then
  local v=redis.call('GET',lk) 
  if ARGV[1]=='1' then
    return {lk,v,redis.call('TTL',lk)}
  else
    return {lk,v}
  end
end
return nil
