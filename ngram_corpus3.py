# coding: UTF-8
import re
import fileinput
import pprint
import MySQLdb
import sys

def split_list(l, n):
    
    #リストをサブリストに分割する
    #:param l: リスト
    #:param n: サブリストの要素数
    #:return: 
    
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]

#データベースに挿入
def detabase_insert(result):
    conn = MySQLdb.connect(
    user='takumi',
    
    passwd='znm6hmv9',
    host='localhost',
    db='research_db'
    )
    
    cursor = conn.cursor()
    for item in result:
        if len(item) == 3:
            cursor.execute("INSERT INTO corpus3 (first_word,second_word,third_word,count3) VALUES (%s,%s,%s,1) ON DUPLICATE KEY UPDATE  count3 = count3 + 1",(item[0],item[1],item[2]))
            print(item)
    conn.commit()
    # 接続を閉じる
    conn.close

#ngram
def ngram(sentense,scale):
    # 変数を用意
    str = ''
    wordlist = []
    #文章から空白で分割
    splited = sentense.split('\t')
    while '\n' in splited:splited.remove('\n')
    #print(splited)
    if scale > len(splited):
        return ""
    else:
        for i in range (0, len(splited)-(scale-1)):
            for ii in range (0, scale):
                if ii == 0:
                    str += splited[ii+i]
                else:
                    str += '\t' + splited[ii+i]
            wordlist.insert(i, str)
            #strの初期化
            str = ''
        return wordlist


#-----プロジェクト名を取得
#-----パス名を取得


args = sys.argv

project_name = args[1]
path_name   =  args[2]


for line in sys.stdin:
    data = ngram(line, 3)
    print(path_name)
    result =list(split_list('\t'.join(data).split('\t'),3))
    #print(result)
    detabase_insert(result)