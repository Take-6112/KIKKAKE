import sqlite3

# service.dbとつなぐ(なければ作られる)
conn = sqlite3.connect('k_post.db')
c = conn.cursor()

# テーブル作成
c.execute("create table users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT , password TEXT)")
c.execute("create table k_posts(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, comment TEXT, del_flag INTEGER, time TEXT, cat_id INTEGER)")
c.execute("create table categories(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")

# 確定
conn.commit()

# バイバイ
conn.close()
