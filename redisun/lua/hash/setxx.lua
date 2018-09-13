local vs={}
local lt=tonumber(ARGV[2])
local ex=ARGV[1]
for i,k in ipairs(KEYS) do
  local st=false
  local tp=redis.call('TYPE',k)['ok']
  if tp=='hash' then
    local ms=redis.call('HMSET',k,_SET_KVS_)['ok']
    if ms=='OK' then
      st=0
      if lt>0 then
        if ex == 'EX' then
          redis.call('EXPIRE',k,lt)
        else
          redis.call('PEXPIRE',k,lt)
        end
      end
    else
      st=2
    end
  else
    st=3
  end
end
return vs
