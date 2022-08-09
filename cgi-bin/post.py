#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import cgi, cgitb, sqlite3, codecs
import io
import sys

# printの出力結果をUTF-8に
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
cgitb.enable()

print("Content-Type: text/html")
print()

form = cgi.FieldStorage()
form_check = 0


dbname = 'timeTable.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS persons(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               studentNumber INTEGER,
               dayOfWeek TEXT,
               lesson TEXT,
               lessonName TEXT)
            """)

cur.execute("""INSERT INTO persons(studentNumber, dayOfWeek, lesson, lessonName) SELECT ?, ?, ?, ?
               WHERE NOT EXISTS(
                 SELECT * 
                 FROM persons
                 WHERE studentNumber=?
                 AND  dayOfWeek=?
                 AND  lesson=?
               )
            """, 
            (form["studentNumber"].value,
            form["dayOfWeek"].value,
            form["lesson"].value,
            form["lessonName"].value,
            form["studentNumber"].value,
            form["dayOfWeek"].value,
            form["lesson"].value))
# 同じコマの奴は上書きする．
cur.execute("UPDATE persons SET lessonName=? WHERE studentNumber=? AND dayOfWeek=? AND lesson=?",
            (form["lessonName"].value,
            form["studentNumber"].value,
            form["dayOfWeek"].value,
            form["lesson"].value))
html = codecs.open('./views/afterPost.html', 'r', 'utf-8').read()
print (html)

conn.commit()

cur.close()
conn.close()

#回避用コメント