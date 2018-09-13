local vs={}
local lt=tonumber(ARGV[2])
for i,k in ipairs(KEYS) do
  local st=false
  local ms=false
  local tp=redis.call('TYPE',k)['ok']
  if tp=='hash' or tp=='none' then
    ms=redis.call('HMSET',k,_SET_KVS_)['ok']
    if ms=='OK' then
      st=0
      if lt>0 then
        if ARGV[1]=='EX' then
          redis.call('EXPIRE',k,lt)
        else
          redis.call('PEXPIRE',k,lt)
        end
      end
    else
      st=2
    end
  else
    st=1
  end
  vs[i]={ k,st,ms }
end
return vs
