Generic single-database configuration.

#### [Alembic](http://alembic.zzzcomputing.com/en/latest/index.html)
Alembic 是[Sqlalchemy](http://docs.sqlalchemy.org/en/latest)的作者实现的一个数据库版本化管理工具,它可以对基于Sqlalchemy的Model与数据库之间的历史关系进行版本化的维护

### 安装Alembic

```bash
pip install alembic
# 也会安装sqlalchemy模块
```

### 实例一个alembic  
```bash
cd create_ev
# 实例化一个alembic,会生成如下的目录结构
alembic init alembic  # 生成一个名为alembic的目录

├── alembic
│   ├── env.py 每次执行Alembic都会加载这个模块,主要提供项目Sqlalchemy Model和数据库的连接
│   ├── README
│   ├── script.py.mako  迁移脚本生成模版
│   └── versions  存放生成的迁移脚本目录
├── alembic.ini  基本的配置(包括数据库连接)

# 本次操作是数据库中还没有表时创建的,所以xx_init.py是创建新表
```
### alembic将model对象连接到数据库中
- 在任意位置编写[models.py模块](../../learn_sqlalchemy/models.py)(要考虑引包时的方便),14L表明哪里对象需要连接
- 修改[alembic.ini文件](../alembic.ini)的39L来连接数据库(也可以在env.py中连接,但前提要删除alembic.ini文件)
- 修改[env.py文件](./env.py):连接model对象+自动生成迁移脚本,29L

### 生成迁移脚本
```bash
# 会根据当前定义的models.py与整个数据库的表结构做对比,然后再生成迁移脚本(类似: django makemigrations)
alembic revision --autogenerate -m "init"

# 更新到最新版本(执行迁移脚本生成数据库: django migrate)
alembic upgrade head
# 默认是从alembic目录下 versions目录生成数据库
```

#### 基本操作命令(根据versions目录的脚本比较进行执行)
```bash
# 升到最高版本
alembic upgrade head

# 降到最初版本
alembic downgrade base

# 升两级
alembic upgrade +2

# 降一级
alembic downgrade -1

# 升级到制定版本
alembic upgrade e93b8d488143

# 查看当前版本
alembic current

# 查看历史版本详情
alembic history --verbose

# 查看历史版本（-r参数）类似切片
alembic history -r1975ea:ae1027
alembic history -r-3:current
alembic history -r1975ea:
```


### 在docker中操作
```bash
docker exec -it webdocker_web_1 bash
# 修改model/models.py文件
alembic revision --autogenerate -m "Article share to server_default"
alembic upgrade head
```

