local ov = redis.call('GET',KEYS[1])
local ttl = redis.call('TTL',KEYS[1])
local lt = tonumber(ARGV[2]) 
local st
if lt==0 and ttl>0 then
    st=redis.call('SET',KEYS[1],ARGV[1],ARGV[3],ttl)
elseif lt>0 then
    st=redis.call('SET',KEYS[1],ARGV[1],ARGV[3],lt)
else
    st=redis.call('SET',KEYS[1],ARGV[1])
end 
return {ov,st}
