local rs={}
for i,k in ipairs(KEYS) do
  local ov = redis.call('GET',k)
  local ttl = redis.call('TTL',k)
  local lt = tonumber(ARGV[2]) 
  if lt==0 and ttl>0 then
      redis.call('SET',k,ARGV[1],ARGV[3],ttl)
  elseif lt>0 then
      redis.call('SET',k,ARGV[1],ARGV[3],lt)
  else
      redis.call('SET',k,ARGV[1])
  end 
  rs[i]={k,ov}
end
return rs
