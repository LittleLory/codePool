#!/usr/bin/python
# coding=utf-8

import urllib2
import re
import json
import sys
import types
import codecs
import chardet
import csv

reload(sys)
sys.setdefaultencoding('utf-8')


resp = urllib2.urlopen('http://car.autohome.com.cn/config/spec/25379.html')
body = resp.read()

model_ids = []
spec_ids = []

config = re.search(r'var specIDs =\[(.*)\];', body)
data = config.group(1)
model_ids = data.split(',')

result = {int(model_id): {} for model_id in model_ids}

print '==============================='

config = re.search(r'var config = (\{.*\});', body)
data = config.group(1)
encoding = chardet.detect(data)['encoding']
j = json.loads(data, encoding=encoding)

for config_types in j['result']['paramtypeitems']:
    for config_items in config_types['paramitems']:
        id = config_items['id']
        if id not in spec_ids: spec_ids.append(id)
        print '------ id[%s] ------' % id
        values = config_items['valueitems']
        for value in values:
            result[value['specid']][id] = value['value']
            print '%s-[%s]' % (value['specid'], value['value'])

print '==============================='

config = re.search(r'var option = (\{.*\});', body)
data = config.group(1)
encoding = chardet.detect(data)['encoding']
j = json.loads(data, encoding=encoding)

for config_types in j['result']['configtypeitems']:
    for config_items in config_types['configitems']:
        id = config_items['id']
        if id not in spec_ids: spec_ids.append(id)
        print '------ id[%s] ------' % id
        values = config_items['valueitems']
        for value in values:
            result[value['specid']][id] = value['value']
            print '%s-[%s]' % (value['specid'], value['value'])

for model_id, details in result.items():
    print '%s\t%s' % (model_id, details)

# f = csv.writer(open('detail.csv', 'w+'))
# title = []
# title.append('model_id')
# title.append(model_ids)
#
#
#
# row = []
# for model_id, details in result.items():
#     row.append(model_id)
#     for spec_id in spec_ids:
#         value = ""
#         if spec_id in details:
#             value = details[spec_id]
#         row.append(value)
#
#     f.writerow(row)


print 'finish...'

