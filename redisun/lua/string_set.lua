local vs = {}
local lt = tonumber(ARGV[3])
for i,k in ipairs(KEYS) do
  local ttl = redis.call('TTL',k)
  if lt == 0 and ttl>0 then
    vs[i] = {k,redis.call('SET',k,ARGV[1],ARGV[2],ttl)}
  elseif lt>0 then
    vs[i] = {k,redis.call('SET',k,ARGV[1],ARGV[2],lt)}
  else
    vs[i] = {k,redis.call('SET',k,ARGV[1])}
  end 
end
return vs
