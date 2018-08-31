local vs={}
local lt = tonumber(ARGV[1])
local ex = ARGV[2]
for i,k in ipairs(KEYS) do
  vs[i] = {k,redis.call('HMSET',k,%s)}
  if lt>0 then
    if ex=='EX' then
      redis.call('EXPIRE',k,lt)
    else
      redis.call('PEXPIRE',k,lt)
    end
  end 
end
return vs
