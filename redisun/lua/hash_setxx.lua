local vs={}
local lt = tonumber(ARGV[1])
local ex = ARGV[2]
for i,k in ipairs(KEYS) do
  if redis.call('EXISTS',k)==1 then
    local ms=redis.call('HMSET',k,%s)
    vs[i]={k,ms}
    if lt>0 then
      if ex=='EX' then
        redis.call('EXPIRE',k,lt)
      else
        redis.call('PEXPIRE',k,lt)
      end
    end 
  else 
    vs[i]={k,nil}
  end
end
return vs
