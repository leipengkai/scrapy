# redis 服务器的统计信息
INFO

# 查看所有redis配置
CONFIG GET *

# 查看redis配置, 日志级别
config get loglevel
# redis 安装目录
CONFIG GET dir

# 下面的命令将在 redis 安装目录中创建dump.rdb文件, 备份当前数据库的数据
save

# 查看是否设置redis密码
CONFIG get requirepass
# CONFIG set requirepass passwd

# 修改配置
# config set loglevel "notice"

flushall 清空所有的数据库的所有数据
keys *  所有数据

select 0  选择数据库:默认有0~15个数据库

# string 最大为512M
设置字符串
set one 1
mset two 2 three 3


获取字符串
get one
mget one two three

setex one 5 "abc"  # 设置多少秒之后过期

append two 22  # 222 之前有key则追加操作,否则则是增加操作

# hash值(存取对象)
设置person对象的一个/多个属性
hset person age 18 gender true name femn

获得对象的所有属性
hkeys person
获得对象所有的属性值
hvals person

获得对象的指定属性值
hget person age 
获得对象的一个/多个属性值
hmget person age name
删除一个/多个属性
hdel person age name


# list
flushall
往列表的左边添加元素
lpush one 1
lpush one 2 3 
lrange one 0 -1

往列表的右边添加元素
rpush one 4 5 


# set集合
sadd learn redis
sadd learn mongo
sadd learn rabbitmq
smembers learn


# zset 有序集合
# redis正是通过分数来为集合中的成员进行从小到大的排序,如果分数相同按字母顺序排序
# zset的成员是唯一的,但分数(score)却可以重复
del learn 
zadd learn 0 redis
zadd learn 0 mongo
zadd learn 0 rabbitmq
ZRANGEBYSCORE learn 0 100

守护线程就是当主线程结束后,也会结束掉守护的线程
