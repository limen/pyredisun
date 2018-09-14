# Make Redis manipulations easy. Unify commands for all data types.

[![Build Status](https://travis-ci.org/limen/redisun-py.svg?branch=master)](https://travis-ci.org/limen/redisun-py)

## First glance

```python
model = StringModel()

######################
# Single key operation
######################

# create a key 'greeting:redisun:0901' with value 'Hello, Redisun!'
# and set its ttl to 100s
model.where('name', 'redisun').where('date', '0901').create('Hello, Redisun!', 100)

# Retrieve the key and its ttl
model.first(True)
# return key, value, ttl
# key - 'greeting:redisun:0901'
# value - 'Hello, Redisun!'
# ttl - 100


#########################
# Multiple keys operation
#########################

# create two keys 'greeting:redisun:0901' and 'greeting:redisun:0902'
# with value 'Hello, Redisun!' and set their ttls to 100s
model.where('name', 'redisun').where_in('date', ['0901', '0902']).create('Hello, Redisun!', 100)

# Retrieve the keys and their ttls
model.all(True)
# returns ok keys, ok keys value, failed keys status, failed keys hint
# ok keys - ['greeting:redisun:0901', 'greeting:redisun:0902'],
# ok keys value - {'greeting:redisun:0901': 'Hello, Redisun!', 'greeting:redisun:0902': 'Hello, Redisun!'},
# failed keys status - {},
# failed keys hint - {}

```


## More

[Wiki](https://github.com/limen/redisun-py/wiki)

[Unit tests](https://github.com/limen/redisun-py/tree/master/tests)

[PHP version](https://github.com/limen/redisun)

