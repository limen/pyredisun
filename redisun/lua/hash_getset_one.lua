local ov
local st
local ms
local tp = redis.call('TYPE', KEYS[1])['ok']
if tp == 'hash' or tp == 'none' then
    if ARGV[1] == '1' then
        ov = redis.call('HMGET', KEYS[1]%s)
    else
        ov = redis.call('HGETALL', KEYS[1])
    end
    local lt = tonumber(ARGV[3])
    ms = redis.call('HMSET', KEYS[1],%s)['ok']
    if lt>0 and ms=='OK' then
        st = 0
        if ARGV[2]=='EX' then
            redis.call('EXPIRE', KEYS[1], lt)
        else
            redis.call('PEXPIRE',KEYS[1], lt)
        end
    end
    if ms~='OK' then
        st = 2
    end
else
    st = 1
end
return {KEYS[1], st, ov, ms}
