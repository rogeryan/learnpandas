#!/usr/bin/env python

from datetime import datetime


#
#
# 将字符串转换为13位的timestamp(含毫秒)
def str2ts(date_string):
    do = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    return int(do.timestamp() * 1000)


#
#
# 将字符串转换为13位的timestamp(含毫秒)
def str2dt(date_string):
    dt = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    return dt


#
#
# 将datetime对象转换为13位的timestamp(含毫秒)
def dt2ts(dt):
    return int(dt.timestamp() * 1000)


#
#
# 将13位的timestamp转换成字符串，例如:2019-09-12 13:22:45
def ts2str(ts):
    dt = datetime.fromtimestamp(ts / 1000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


