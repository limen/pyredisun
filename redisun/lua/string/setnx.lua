local vs={}
local lt=tonumber(ARGV[3])
for i,k in ipairs(KEYS) do
  local tp=redis.call('TYPE',k)['ok']
  local st=1
  local ms
  local ttl
  if tp == 'none' then
    st=0
    if ARGV[3] == 'EX' then
      ttl=redis.call('TTL',k)
    else
      ttl=redis.call('PTTL',k)
    end
    if lt == 0 and ttl > 0 then
      ms=redis.call('SET',k,ARGV[1],ARGV[2],ttl)['ok']
    elseif lt > 0 then
      ms=redis.call('SET',k,ARGV[1],ARGV[2],lt)['ok']
    else
      ms=redis.call('SET',k,ARGV[1])['ok']
    end
    if ms ~= 'OK' then
      st=2
    end
  elseif tp == 'string' then
    st=3
  end
  vs[i]={ k,st,ms }
end
return vs
