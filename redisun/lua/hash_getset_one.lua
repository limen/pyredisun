local ov
if ARGV[1]=='1' then
  ov=redis.call('HMGET',KEYS[1]%s)
else
  ov=redis.call('HGETALL',KEYS[1])
end
local lt=tonumber(ARGV[2]) 
local ms=redis.call('HMSET',KEYS[1],%s)
if lt>0 and ms=='OK' then
  if ARGV[3]=='EX' then
    redis.call('EXPIRE',KEYS[1],lt)
  else 
    redis.call('PEXPIRE',KEYS[1],lt)
  end
end 
return {KEYS[1],ov,ms}
