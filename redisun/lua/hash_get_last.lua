local lk
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    lk=k
  end
end
if lk~=nil then
  local v
  local vr
  if ARGV[1]=='1' then
    v=redis.call('HMGET',k%s)
  else
    v=redis.call('HGETALL',lk)
  end
  if ARGV[2]=='1' then
    if ARGV[3]=='EX' then
      vr={lk,v,redis.call('TTL',lk)}
    else
      vr={lk,v,redis.call('PTTL',lk)}
    end
  else
    vr={lk,v}
  end
  return vr
end
return nil
