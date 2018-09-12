local vs = {}
for i, k in ipairs(KEYS) do
    local ov
    local st
    local ms
    local tp = redis.call('TYPE', k)['ok']
    if tp == 'hash' then
        st = 0
        if ARGV[1] == '1' then
            ov = redis.call('HMGET', k%s)
        else
            ov = redis.call('HGETALL', k)
        end
    elseif tp == 'none' then
        st = 0
    else
        st = 1
    end
    if tp == 'hash' or tp == 'none' then
        local lt = tonumber(ARGV[3])
        ms = redis.call('HMSET', k,%s)['ok']
    if lt>0 and ms=='OK' then
    if ARGV[2]=='EX' then
        redis.call('EXPIRE', k, lt)
        else
        redis.call('PEXPIRE', k, lt)
        end
        end
    end
    vs[#vs + 1] = { k, st, ov, ms }
end
return vs
