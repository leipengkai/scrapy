#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, sessionmaker, undefer, aliased
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

MYSQL_DB = "scrapy"
MYSQL_HOST = "0.0.0.0"
MYSQL_PAWD = "123456"
MYSQL_PORT = "3307"
MYSQL_USER = "root"

Base = declarative_base()


class MessageLogs(Base):
    """
    消息日志表
    """
    __tablename__ = 'message_logs'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)
    target = Column(String(256))  # mobile email
    verification_code = Column(String(16))
    routing_key = Column(String(256),
                         server_default='')  # 自定义邮件模板(对应MessageTemplate表的routing_key字段) ,同时也对应消费者处理业务逻辑的方法 eg "email_info" "sms_register"
    template_code = Column(String(16), server_default='')  # 阿里云短信模板 eg TemplateCode:SMS_166777256
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    platform = Column(String(16))  # 
    type = Column(String(16), server_default='')  # "sms" "email"


class MessageTemplate(Base):
    """
    邮件消息模板(短信模板暂时没有加入)
    """
    __tablename__ = 'message_template'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)
    content = Column(String(256))
    routing_key = Column(String(256), unique=True)  # "email_info"
    create_time = Column(DateTime, default=datetime.datetime.utcnow)


class MysqlClient():

    def __init__(self, user=MYSQL_USER, password=MYSQL_PAWD, host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_DB):
        # pip install SQLAlchemy pymysql
        engine_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(user, password, host, port, db)
        self.db_engine = create_engine(engine_url, echo=True)

        db_pool = sessionmaker(bind=self.db_engine)  # 负责执行内存中的对象和数据库表之间的同步工作
        self.session = db_pool()  # 先使用工程类来创建一个session

    def create_table(self):
        Base.metadata.create_all(self.db_engine)

    def test_add_log(self):
        c1 = MessageLogs(target=TESTMOBILE, verification_code='88888', template_code='SMS_166777256', platform="拍拍印")
        self.session.add(c1)
        self.session.commit()
        # print(session.query(MessageLogs).first())

    def test_add_template(self):
        content = """ <p>你好,邮件发送的信息:{}</p> """
        c1 = MessageTemplate(content=content, routing_key="email_info")
        self.session.add(c1)
        self.session.commit()

    def test_get_template(self):
        q = self.session.query(MessageTemplate).filter(MessageTemplate.routing_key == "email_info").first()
        print(q)

    def add(self, target, type, code, routing_key, template_code="", platform="拍拍印"):
        c1 = MessageLogs(target=target, type=type, verification_code=code, routing_key=routing_key,
                         template_code=template_code, platform=platform)
        self.session.add(c1)
        self.session.commit()

    def get_template(self, routing_key):
        query = self.session.query(MessageTemplate).filter(MessageTemplate.routing_key == routing_key).first()
        if query:
            return query.content
        else:
            return """ <p>默认模板{}</p> """

    ############################### create table for sql:https://my.oschina.net/u/111188/blog/1524541
    # def connect_mysql(self):
    #     db_conn = self.db_engine.connect()
    #     db_conn.execute(r''' CREATE TABLE IF NOT EXISTS sms_logs (
    #             mobile char(11),
    #             template_code char(16),
    #             message varchar(256),
    #             create_time timestamp NOT NULL DEFAULT NOW(),
    #             platform char(16),
    #             log_mark varchar(256))
    #             ''')
    #     db_conn.close()
    #     print("ok")
    ################################ create table for sql


if __name__ == '__main__':
    client = MysqlClient()
    # client.create_table()

    # client.test_add_log()
    client.test_add_template()

    # client.test_get_template()
