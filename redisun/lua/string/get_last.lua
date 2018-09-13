local lk=false
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k) == 1 and redis.call('TYPE',k)['ok'] == 'string' then
    lk=k
  end
end
if lk ~= false then
  local v=redis.call('GET',lk)
  local ttl=false
  if ARGV[1] == '1' then
    if ARGV[2] == 'EX' then
      ttl=redis.call('TTL',lk)
    else
      ttl=redis.call('PTTL',lk)
    end
  end
  return { lk,v,ttl }
end
return nil
