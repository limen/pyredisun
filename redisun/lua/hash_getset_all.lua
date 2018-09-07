local vs={}
for i,k in ipairs(KEYS) do
  local ov=nil
  if ARGV[1]=='1' then
    ov=redis.call('HMGET',k%s)
  else
    ov=redis.call('HGETALL',k)
  end
  local lt=tonumber(ARGV[2]) 
  local ms=redis.call('HMSET',k,%s)
  if lt>0 and ms=='OK' then
    if ARGV[3]=='EX' then
      redis.call('EXPIRE',k,lt)
    else 
      redis.call('PEXPIRE',k,lt)
    end
  end 
  vs[#vs+1]={k,ov,ms}
end
return vs
