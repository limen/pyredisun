local fk
for i, k in ipairs(KEYS) do
    if redis.call('EXISTS', k) == 1 and redis.call('TYPE', k)['ok'] == 'hash' then
        fk = k
    end
end
if fk ~= nil then
    local v
    local ttl
    if ARGV[1] == '1' then
        v = redis.call('HMGET', fk%s)
    else
        v = redis.call('HGETALL', fk)
    end
    if ARGV[2] == '1' then
        if ARGV[3] == 'EX' then
            ttl = redis.call('TTL', fk)
        else
            ttl = redis.call('PTTL', fk)
        end
    end
    return { fk, v, ttl }
end
return nil
