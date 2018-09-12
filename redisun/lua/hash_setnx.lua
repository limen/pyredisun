local vs = {}
local lt = tonumber(ARGV[2])
local ex = ARGV[1]
for i, k in ipairs(KEYS) do
    if redis.call('EXISTS', k) == 0 then
        local ms=redis.call('HMSET',k,%s)['ok']
        if lt > 0 and ms == 'OK' then
            if ex == 'EX' then
                redis.call('EXPIRE', k, lt)
            else
                redis.call('PEXPIRE', k, lt)
            end
            vs[i] = { k, 0, ms }
        else
            vs[i] = { k, 2, ms }
        end
    else
        vs[i] = { k, 1, nil }
    end
end
return vs
