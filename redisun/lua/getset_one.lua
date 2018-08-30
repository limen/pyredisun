local ov = redis.call('GET',KEYS[1])
local ttl = redis.call('TTL',KEYS[1])
local lt = tonumber(ARGV[2]) 
if lt==0 and ttl>0 then
    redis.call('SET',KEYS[1],ARGV[1],ARGV[3],ttl)
elseif lt>0 then
    redis.call('SET',KEYS[1],ARGV[1],ARGV[3],lt)
else
    redis.call('SET',KEYS[1],ARGV[1])
end 
return ov
