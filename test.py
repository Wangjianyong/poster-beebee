#!/usr/bin/python

import zhihu
import time

if __name__ == '__main__':
    connector = zhihu.zhihu()
    connector.login(account="wjy5095844@sina.com", password="wjy13852873220")
    time.sleep(2)
    connector.logout()
