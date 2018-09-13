local vs = {}
for i, k in ipairs(KEYS) do
    local ov
    local st
    local ms
    local ttl
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
        if ARGV[2] == 'EX' then
            ttl = redis.call('TTL', k)
        elseif ARGV[2] == ('PX') then
            ttl = redis.call('PTTL', k)
        end
        local lt = tonumber(ARGV[3])
        ms = redis.call('HMSET', k,%s)['ok']
        if lt > 0 and ms == 'OK' then
            if ARGV[2] == 'EX' then
                redis.call('EXPIRE', k, lt)
            else
                redis.call('PEXPIRE', k, lt)
            end
        end
    end
    vs[i] = { k, st, ov, ttl, ms }
end
return vs
