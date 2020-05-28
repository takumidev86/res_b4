# coding: UTF-8
import re
import fileinput
import pprint
import MySQLdb
import mysql.connector
import sys
import math

def split_list(l, n):
    
    #リストをサブリストに分割する
    #:param l: リスト
    #:param n: サブリストの要素数
    #:return: 
    
    for idx in range(0, len(l), n):
        yield l[idx:idx + n]


#クロスエントロピーを計算
def cross_entropy(cursor,select1,select2,select3,select4,insert,project_name, path_name, result,num,num_line_count):

    entropy_sum = 0
    for item in result:
        if len(item) == 3:
            #print('----------')
            #ノーマルngramモデル；SELECT文でfirst_wordとsecond_wordが一致する合計を代入
            #cursor.execute("SELECT SUM(pro_file_wordcount) FROM corpus WHERE first_word = %s AND second_word = %s",item2)
            cursor.execute(select1,(item[0],item[1]))
            #print("select1")
            ngram2_count = int(re.sub("\\D", "",str(list(cursor.fetchone()))))
            #ノーマルngramモデル；SELECT文でfirst_wordとsecond_wordとthird_wordが一致する合計を代入
            #cursor.execute("SELECT SUM(pro_file_wordcount) FROM corpus WHERE first_word = %s AND second_word = %s  AND third_word = %s",item)
            cursor.execute(select2,(item[0],item[1],item[2]))
            #print("select2")
            ngram3_count = int(re.sub("\\D", "",str(list(cursor.fetchone()))))
            #キャッシュモデル；SELECT文でプロジェクト名とfirst_wordとsecond_wordが一致する合計を代入
            #cursor.execute("SELECT SUM(pro_file_wordcount) FROM corpus WHERE project_name = %s AND first_word = %s AND second_word = %s",(project_name,item2[0],item2[1]))
            cursor.execute(select3,(project_name,item[0],item[1]))
            #print("select3")
            cache2_count = int(re.sub("\\D", "",str(list(cursor.fetchone()))))
            #キャッシュモデル；SELECT文でプロジェクト名とfirst_wordとsecond_wordが一致する合計を代入
            #cursor.execute("SELECT SUM(pro_file_wordcount) FROM corpus WHERE project_name = %s AND first_word = %s AND second_word = %s AND third_word = %s",(project_name,item[0],item[1],item[2]))
            cursor.execute(select4,(project_name,item[0],item[1],item[2]))
            #print("select4")
            cache3_count = int(re.sub("\\D", "",str(list(cursor.fetchone()))))
            entropy_sum = entropy_sum + entropy(ngram2_count,ngram3_count,cache2_count,cache3_count)
            #print("entropy")
    #クロスエントロピーを計算
    cross_entropy = -(entropy_sum / len(result))
    print(path_name)
    #print(result)
    #行番号num
    print(num)
    #num行のトークン数num_line_count
    # print("crossentropy")
    print(cross_entropy)
    bool_bit = 0
    #cursor.execute("INSERT INTO cross_entropy (file_path,file_line_number,token_count,bool_bit,entropy)VALUES (%s,%s,%s,%s,%s)",(path_name,num,num_line_count,bool_bit,cross_entropy))
    cursor.execute(insert,(path_name,num,num_line_count,bool_bit,cross_entropy))
    
    conn.commit()
    # print("insert")


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

#登場確率を計算
def entropy(ngram2_count,ngram3_count,cache2_count,cache3_count):
    ganma = 1

    return math.log2(((ganma/(ganma + cache3_count))*(ngram3_count/ngram2_count)) + ((cache3_count/(ganma + cache3_count))*(cache3_count/cache2_count)))
#-----プロジェクト名を取得
#-----パス名を取得


args = sys.argv
project_name = args[1]
path_name   =  args[2]

num  = 0
conn = mysql.connector.MySQLConnection(
    user='takumi',
    passwd='znm6hmv9',
    host='localhost',
    db='research_db'
)

cursor = conn.cursor(prepared=True)

select1 = "SELECT SUM(count2) FROM corpus2 WHERE first_word = ? AND second_word = ?"
select2 = "SELECT SUM(count3) FROM corpus3 WHERE first_word = ? AND second_word = ?  AND third_word = ?"
select3 = "SELECT SUM(pro_file_wordcount) FROM corpus_ WHERE project_name = ? AND first_word = ? AND second_word = ?"
select4 = "SELECT SUM(pro_file_wordcount) FROM corpus_ WHERE project_name = ? AND first_word = ? AND second_word = ? AND third_word = ?"
insert = "INSERT INTO cross_entropy_sample (file_path,file_line_number,token_count,bool_bit,entropy)VALUES (?,?,?,?,?)"

print(path_name)
for line in sys.stdin:
    num_line_count = len(line.split())
    num = num + 1
    data = ngram(line, 3)
    #print(data)
    result =list(split_list('\t'.join(data).split('\t'),3))
    #print(result)
    cross_entropy(cursor,select1,select2,select3,select4,insert,project_name,path_name,result,num,num_line_count)

# 接続を閉じる
conn.close
