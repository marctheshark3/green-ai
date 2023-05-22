#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 08:15:36 2023

@author: marctheshark
"""

import json


class JSONReader:

    def __init__(self, path, file):
        self.path = path
        self.file = file

    def collect(self):
        json_ls = []
        with open('{}/{}'.format(self.path, self.file)) as lines:
            for obj in lines:
                data = json.loads(obj)
                json_ls.append(data)

        return json_ls

    def create_df(self):
        pass

if __name__ == '__main__':
    from pandas import DataFrame
    from datetime import datetime
    json_reader = JSONReader('../data', 'stream_data.json')

    data = json_reader.collect()

    df = DataFrame.from_dict(data)
    col = [item.split('/')[-1] for item in df.columns]
    df.columns = col
    df['time'] = df['time'] / 1000

    df['year'] = [datetime.fromtimestamp(item).year for item in df.time]
    df['month'] = [datetime.fromtimestamp(item).month for item in df.time]
    df['weekday'] = [datetime.fromtimestamp(item).weekday() for item in df.time]
    df['day'] = [datetime.fromtimestamp(item).day for item in df.time]
    df['hour'] = [datetime.fromtimestamp(item).hour for item in df.time]
    df['minute'] = [datetime.fromtimestamp(item).minute for item in df.time]
    df['microsecond'] = [datetime.fromtimestamp(item).microsecond for item in df.time]
