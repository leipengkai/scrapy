## 启动mysql服务
```bash
# 在docker-compose.yml这个文件的目录下运行
docker-compose up
```

## 创建数据库:
```bash
# 进入mysql容器
docker exec -it scrapy_mysql_1 bash
# 连接mysql数据库
mysql -h0.0.0.0 -uroot -p123456
CREATE DATABASE `test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
- 在使用.sql备份文件,导入备份数据之前创建(mongo没有数据库也可以导入备份数据)
- 在mysql创建表
- 使用alembic或者python3 manage.py makemigrations 初始化表之前,如果没有创建,则会自己创建默认字符集的数据库
- 所以这种方法创建的数据库,则需要改成自己想要的字符集格式

## 创建数据
### 使用mysql图形界面或者使用myql命令导入数据
如果是使用docker启动mysql,则需要将test.sql放入database/mysql/的目录下
```bash
docker exec -it scrapy_mysql_1 bash
cd /var/lib/mysql
mysql -h0.0.0.0 -uroot -p123456 test < test.sql
```

### 或者使用手动创建表以及数据
- 创建表: [mysql语句创建表](./create_table),[alembic初始化表以及其它基本操作](./alembic/README.md)
- [mysql语句插入数据](./create_data)


