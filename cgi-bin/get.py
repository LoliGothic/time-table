#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import cgi, cgitb, sqlite3, codecs
import io
import sys

# printの出力結果をUTF-8に
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# トレースバックを得るためにcgitbを有効化する。
cgitb.enable()

print("Content-Type: text/html")
print()

form = cgi.FieldStorage()
form_check = 0


# データベースの接続設定
dbname = 'timeTable.db'  # データベースのファイル名
conn = sqlite3.connect(dbname) # 接続するデータベースの指定
cur = conn.cursor() # Cursorインスタンスの作成
cur.execute("""CREATE TABLE IF NOT EXISTS persons(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               studentNumber INTEGER,
               dayOfWeek TEXT,
               lesson TEXT,
               lessonName TEXT)
            """)
cur.execute("""SELECT * 
              FROM persons
            """)
d_list = cur.fetchall()

# html形式の出力を得る
result = '''
<table border="1">
<tr>
<th>時間割</th>
<th>月</th>
<th>火</th>
<th>水</th>
<th>木</th>
<th>金</th>
</tr>
'''
arrayDayOfWeed = ["月", "火", "水", "木", "金"]
for i in range(1,6):
  result += "<tr>"
  result += "<td>" + str(i) + "</td>"
  for j in arrayDayOfWeed:
    flag = True
    for data in d_list:
      if(i == int(data[3]) and j == str(data[2]) and int(form["showStudentNumber"].value) == int(data[1])):
        result += "<td>" + str(data[4]) + "</td>"
        flag = False
    if flag:
      result += "<td></td>"
  result += "</tr>"

html = codecs.open('./views/afterGet.html', 'r', 'utf-8').read()
html = html.replace('{% result %}', result)

print(html)

conn.commit()

cur.close()
conn.close()

#回避用コメント