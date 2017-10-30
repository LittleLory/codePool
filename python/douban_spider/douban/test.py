#!/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv

book_name_file = csv.reader(open('data/book_name.csv', 'r'))
douban_file = open('data/douban.dat', 'r')

filter_file = open('data/target.dat', 'w+')

target_books = {}
for row in book_name_file:
    target_books[row[1]] = row[0]


for line in douban_file.readlines():
    user_id, book_id, star = line.split('\t')
    if book_id in target_books:
        filter_file.write(line)


