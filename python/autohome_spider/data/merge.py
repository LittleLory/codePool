#!/usr/bin/python
# coding=utf-8

import json
import csv
import codecs
import types
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

brandList = json.loads(open('brand_2017-07-19T03-22-42.json').read())
seriesList = json.loads(open('series_2017-07-19T03-24-17.json').read())
modelList = json.loads(open('model_2017-07-19T03-25-04.json').read())
specList = json.loads(open('spec_2017-07-19T10-09-46.json').read())

brandDict = {brand['id']: brand for brand in brandList}
seriesDict = {series['id'].strip('s'): series for series in seriesList}
# modelDict = {model['id']: model for model in modelList}
specDict = {spec['id']: spec for spec in specList}


specKeys = []
for spec in specList:
    detail = spec['spec']
    for key in detail.keys():
        if key not in specKeys:
            specKeys.append(key)


f = codecs.open('merge.csv', 'w+', 'utf-8')
writer = csv.writer(f)

titles = ['品牌ID', '品牌名称', '车系ID', '车系名称', '车型ID', '车型名称']

for key in specKeys:
    titles.append(key)

writer.writerow(titles)

for model in modelList:
    modelId = model['id']
    modelName = model['name']
    seriesId = model['series_id']
    # print seriesId
    series = seriesDict[seriesId]
    seriesName = series['name']
    brandId = series['brand_id']
    brand = brandDict[brandId]
    brandName = brand['name']

    row = [brandId, brandName, seriesId, seriesName, modelId, modelName]

    spec = specDict[unicode(modelId)]
    if spec:
        detail = spec['spec']
        for key in specKeys:
            value = ""
            if key in detail:
                value = detail[key]
            row.append(value)

    writer.writerow(row)

print 'finish..'

