# -*- coding: utf-8 -*-
import os


if __name__ == '__main__':
    """
    去掉重复的名字
    """
    res_list = []
    f = open(os.path.join(os.getcwd(), 'scrapyname'), 'r') # 爬下来的文件
    res_dup = []

    index = 0
    file_dul = open(os.path.join(os.getcwd(), 'duplicates_name'), 'w') # 重复名的文件
    for line in f.readlines():
        index = index + 1
        if line in res_list:
            temp_str = ""
            temp_str = temp_str + str(index)  # 要变为str才行
            temp_line = ''.join(line)
            temp_str = temp_str + temp_line
            # 最终要变为str类型
            file_dul.write(temp_str)  # 将重复的存入到文件中
        else:
            res_list.append(line)

    for i in res_list:
        with open(os.path.join(os.getcwd(), 'user_name_all'), 'a') as f: # 最终完整且不重复的名字 文件
            f.write(i.replace('i',''))
    print(len(res_list))
