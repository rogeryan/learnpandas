#!/usr/bin/env python

import pymongo
import utils
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

mgclient = pymongo.MongoClient("mongodb://192.168.199.2:27017/")
mgdb = mgclient["hbmarket"]
eth1min = mgdb["eth1min"]


def get_latest(ts):
    result = []
    docs = eth1min.find({"ts": {"$gt": ts}}).sort("ts")
    for doc in docs:
        result.append(doc['tick'])
    return result


#
#
# 获取从dt_start开始，持续时间为duration分钟的数据
def data_from(dt_start, duration=0):
    result = []
    if duration > 0:
        dt_end = dt_start + datetime.timedelta(minutes=duration)
        docs = eth1min.find({"ts": {"$gt": utils.dt2ts(dt_start)}, "ts": {"$lt": utils.dt2ts(dt_end)}})
    else:
        docs = eth1min.find({"ts": {"$gt": utils.dt2ts(dt_start)}})

    last = docs[0]['ts']
    for doc in docs:
        temp = doc['tick']
        del temp['id']
        del temp['mrid']
        temp['ts'] = doc['ts']
        temp['tsg'] = doc['ts'] - last
        last = doc['ts']
        result.append(temp)
    return result


#
#
# 获取从ts_from(13位时间戳）开始，持续时间为duration分钟的数据
def data_from_ts(ts_from, duration=10):
    return data_from(dt=datetime.fromtimestamp(ts_from / 1000), duration=duration)


class Chaser:
    def __init__(self):
        self.data = None
        self.rows = []
        self.rows_max = 100
        self.bb_count = 20
        self.bb_height = 2

    def add_row(self, row):
        # if len(self.rows) > self.rows_max:
        #     self.rows.pop(0)
        self.rows.append(row)

    def add_all(self, rows):
        self.rows.extend(rows)

    def boll_band(self):
        self.data = pd.DataFrame(self.rows)
        print(self.data.describe())
        mid = self.data.iloc[-self.bb_count:, 1].mean()
        std = self.data.iloc[-self.bb_count:, 1].std()
        print(mid, std, self.bb_height * std)
        upper = mid + self.bb_height * std
        lower = mid - self.bb_height * std
        return [upper, mid, lower]


def tester():
    chaser = Chaser()
    start = utils.str2dt('2019-05-29 22:20:00')
    data = data_from(start)
    chaser.add_all(data)
    logging.info(chaser.boll_band())


if __name__ == "__main__":
    tester()
    # r = get_latest(utils.str2ts('2019-05-23 22:20:00'))
    # for d in r:
    #     print(d)
    # print(f'获取到{len(r)}条数据.')
