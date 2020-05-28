# coding: UTF-8
import re
import fileinput
import pprint
import MySQLdb
import mysql.connector
import sys
import math


args = sys.argv
c2_file = args[1]

conn = mysql.connector.MySQLConnection(
    user='takumi',
    passwd='znm6hmv9',
    host='localhost',
    db='research_db'
)

cursor = conn.cursor(prepared=True)




select1 = "SELECT SUM(count) FROM corpus_3 WHERE first_word = ? AND second_word = ?"
select2 = "SELECT SUM(pro_file_wordcount) FROM corpus_ WHERE first_word = ? AND second_word = ?  AND third_word = ?"
insert1 ="insert into corpus2(first_word,second_word,count) values(?,?,?)"
insert2 ="insert into corpus3(first_word,second_word,third_word,count) values(?,?,?,?)"

a = 0
with open(c2_file) as f:
    line_all = f.readlines()
for line in line_all:
    line = line.rstrip('\n')
    line = line.rstrip('\r')
    tokens = line.split('\t')
    print(tokens)
    cursor.execute(select1,(tokens[0],tokens[1]))
    count = int(re.sub("\\D", "",str(list(cursor.fetchone()))))
    print(count)
    a = a + 1
    print(a)
    cursor.execute(insert1,(tokens[0],tokens[1],count))
conn.commit()

# 接続を閉じる
conn.close
