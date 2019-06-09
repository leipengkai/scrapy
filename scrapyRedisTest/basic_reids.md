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

集合

有序集合

守护线程就是当主线程结束后,也会结束掉守护的线程
