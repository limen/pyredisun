local rs={}
for i,k in ipairs(KEYS) do
  local ov = redis.call('GET',k)
  local ttl = redis.call('TTL',k)
  local lt = tonumber(ARGV[2])
  local st
  if lt==0 and ttl>0 then
      st=redis.call('SET',k,ARGV[1],ARGV[3],ttl)
  elseif lt>0 then
      st=redis.call('SET',k,ARGV[1],ARGV[3],lt)
  else
      st=redis.call('SET',k,ARGV[1])
  end 
  rs[i]={k,ov,st}
end
return rs
