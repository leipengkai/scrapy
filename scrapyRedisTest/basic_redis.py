import redis

# 1.链接数据库 key--value
client = redis.StrictRedis(host='0.0.0.0', port=6380, db=1) #  password='admin123'

# 2.设置key
key = 'pyone'

# 3.string  增加
result = client.set(key, "1")

# 4.删 1, 0
# result = client.delete(key)


# 5.改
result = client.set(key,'2')


# 6.查--bytes
result = client.get(key)

# 查看所有的键
result = client.keys()

print(result)
