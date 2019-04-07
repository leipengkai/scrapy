""" -*- coding: utf-8 -*- """
from scrapy import cmdline

import os
import sys

if __name__ == '__main__':
    # sys.path.append(os.path.dirname(os.path.abspath(__file__))) # pychram调试
    cmdline.execute('scrapy crawl instagram'.split())
