local tp=redis.call('TYPE',KEYS[1])['ok']
local st=1
local ov
local ms
if tp == 'string' or tp == 'none' then
  st=0
end
if st == 0 then
  ov=redis.call('GET',KEYS[1])
  local ttl
  if ARGV[3] == 'EX' then
    ttl=redis.call('TTL',KEYS[1])
  else
    ttl=redis.call('PTTL',KEYS[1])
  end
  local lt=tonumber(ARGV[3])
  if lt == 0 and ttl > 0 then
    ms=redis.call('SET',KEYS[1],ARGV[1],ARGV[2],ttl)['ok']
  elseif lt > 0 then
    ms=redis.call('SET',KEYS[1],ARGV[1],ARGV[2],lt)['ok']
  else
    ms=redis.call('SET',KEYS[1],ARGV[1])['ok']
  end
end
if ms ~= 'OK' then
  st=2
end
return { KEYS[1],st,ov,ms }
