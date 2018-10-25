# -*- coding: utf-8 -*-
import random
import os

import pymysql
from datetime import datetime

conn = pymysql.connect(host='11',
                       port=3306,
                       user='root',
                       passwd='1',
                       db='qhh',
                       charset="utf8"
                       )

cur = conn.cursor()

query = ("SELECT * FROM users_userprofile")

add_user_query = ("INSERT INTO users_userprofile"
            "(first_name,last_name,name,birthday,email,\
            password,username,gender,mobile,image,date_joined,\
            is_superuser,is_staff,is_active,voucher_num) "

            "VALUES (%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s)"
            )

delete_user_query = ("DELETE FROM users_userprofile WHERE is_superuser='88' and mobile='00000000000' and image like 'users/test/%'")

def select_user():
    cur.execute(query)
    for r in cur:
        # for r in cur.fetchall():
        print(r)
    cur.close()
    conn.close()

def add_user():
    a= datetime.now()
    index = 3810 #1985,3810
    f = open(os.path.join(os.getcwd(), 'user_name_all'), 'r')
    for line in f.readlines():
        # print(line.replace("\n", "")) #where  username like "萌神%";
        # 但插入到数据库中的是带换行了,可进一步保证不会与真实用户名重复
        index = index + 1

        user_data = ("",
                    "",
                    None,
                    None,
                    None,
                    "pbkdf2_sha256$36000$zVxZawXWSbG3$L/YPuNX0b7BTsSOo99K+vn0gd3lc+XdwpJh1sHcShzY=",
                    "{}".format(line),
                    random.choice(("female","male")),
                    "00000000000",
                    "users/test/{}.jpg".format(index),
                    datetime.now(),
                    "88",
                    "0",
                    "1",
                     "0",
                    )
        try:
            cur.execute(add_user_query,user_data)
            conn.commit()
            print(line.replace("\n", ""))  # where  username like "萌神%";
        except Exception as e:
            print(e)
            # 发生错误时回滚
            conn.rollback()
    cur.close()
    conn.close()
    print(datetime.now() -a)
    print("上传成功")

def delete_user():
    try:
        # 执行SQL语句
        cur.execute(delete_user_query)
        # 提交修改
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()

    # 关闭连接
    conn.close()
    print('删除成功')


if __name__ == '__main__':
    """
    增加虚拟用户
    """
    # select_user()
    # delete_user()
    add_user()
    pass




