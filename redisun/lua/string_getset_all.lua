local rs = {}
for i, k in ipairs(KEYS) do
    local tp = redis.call('TYPE', k)['ok']
    local ov
    local st
    local ms
    if tp == 'string' then
        ov = redis.call('GET', k)
    end
    if tp == 'string' or tp == 'none' then
        st = 0
    else
        st = 1
    end
    local ttl = redis.call('TTL', k)
    local lt = tonumber(ARGV[3])
    if st == 0 then
        if lt == 0 and ttl > 0 then
            ms = redis.call('SET', k, ARGV[1], ARGV[2], ttl)['ok']
        elseif lt > 0 then
            ms = redis.call('SET', k, ARGV[1], ARGV[2], lt)['ok']
        else
            ms = redis.call('SET', k, ARGV[1])['ok']
        end
    end
    if ms ~= 'OK' then
        st = 2
    end
    rs[i] = { k, st, ov, ttl, ms}
end
return rs
