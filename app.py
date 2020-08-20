# Flaskからimportしてflaskを使えるようにする
from flask import Flask,render_template,request,redirect,session
import sqlite3

#appっていう名前でFlaskアプリをつくっていくよ～みたいな
app = KIKKAKE(__name__)

#シークレットキー設定（sssionが使えるようになる！）
app.secret_key = "sunabaco"




# /pege_1 と入れる pege_1.htmlにとぶ
@app.route("/pege_1)
def page_1():
    return render_template("pege_1.html")

# /pege_2 と入れる pege_2.htmlにとぶ
@app.route("/pege_2")
def page_2():
    return render_template("pege_2.html")

# /pege_3 と入れる pege_3.htmlにとぶ
@app.route("/pege_3")
def page_3():
    return render_template("pege_3.html")

# /pege_4 と入れる pege_4.htmlにとぶ
@app.route("/pege_4")
def page_4():
    return render_template("pege_4.html")

# dbに接続！
@app.route("/db")
def dbtest():
    conn = sqlite3.connect("k_post.db")
    c = conn.cursor()


# # リスト
# @app.route("/list")
# def post_list():
#     if "id" in session:
#         id = session["id"]
#         conn = sqlite3.connect("k_post.db")
#         c = conn.cursor()
#         c.execute("SELECT id FROM users where id = ?",(user_id,))
#         user_
#          = c.fetchone()[0]
#         c.execute("SELECT * FROM task where user_id = ?",(user_id,))
#         task_list = []
#         for row in c.fetchall():
#             task_list.append({"id":row[0],"task":row[1],"limit":row[2]})
#         c.close()
#         print(task_list)
#         return render_template("tasklist.html" , task_list = task_list , user_name = user_name )
#     else:
#         return redirect("/login")


# # 追加機能
# @app.route("/add" , methods=["GET"])
# def add_get():
#     return render_template("add.html")

# @app.route("/add" , methods=["POST"])
# def add_post():
#     if "user_id" in session:
#         user_id = session["user_id"]
#         task = request.form.get("task")
#         limit = request.form.get("limit")
#         print(task)
#         conn = sqlite3.connect("task_list.db")
#         c = conn.cursor()
#         c.execute("INSERT INTO task VALUES(NULL,?,?,?)",(task,limit,user_id))
#         conn.commit()
#         c.close()
#         return redirect("/list")
#     else:
#         return redirect("/login")

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404

# # 編集機能(フォーム表示)
# @app.route("/edit/<int:id>")
# def edit(id):
#     if "user_id" in session:
#         conn = sqlite3.connect("k_post.db")
#         c = conn.cursor()
#         c.execute("SELECT task,limit_task,user_id FROM task where id = ?",(id,))
#         task = c.fetchone()
#         conn.close()
#         print(task)
#         if task is not None:
#             task_name = task[0]
#             limit =task[1]
#             user_id =task[2]
#         else:
#             return "アイテムがありません"

#         item = {"id":id,"task":task_name,"limit":limit,"user_id":user_id}
#         return render_template("edit.html",task = item)
#     else:
#         return redirect("/login")

# # 編集機能（書き換え）
# @app.route("/edit" , methods=["POST"])
# def update_task():
#     if "user_id" in session:
#         task = request.form.get("task")
#         limit = request.form.get("limit")
#         task_id = request.form.get("task_id")
#         print(task)
#         conn = sqlite3.connect("task_list.db")
#         c = conn.cursor()
#         c.execute("UPDATE task SET task = ?,limit_task = ? where id = ?",(task,limit,task_id))
#         conn.commit()
#         c.close()
#         return redirect("/list")
#     else:
#         return redirect("/login")

# # 削除機能
# @app.route("/del/<int:id>")
# def del_task(id):
#     if "user_id" in session:
#         conn = sqlite3.connect("task_list.db")
#         c = conn.cursor()
#         c.execute("DELETE FROM task where id = ?",(id,))
#         conn.commit()
#         conn.close()
#         return redirect("/list")
#     else:
#         return redirect("/login")

# # ユーザー登録機能
# @app.route("/regist")
# def regist_get():
#     return render_template("regist.html")

# @app.route("/regist" , methods=["POST"])
# def regis_post():
#     name = request.form.get("name")
#     password = request.form.get("password")
#     conn = sqlite3.connect("task_list.db")
#     c = conn.cursor()
#     c.execute("INSERT INTO users VALUES(NULL,?,?)",(name,password))
#     conn.commit()
#     c.close()
#     return redirect("/list")

# # ログイン機能
# @app.route("/login")
# def login_get():
#     if "user_id" in session :
#         return redirect("/list")
#     else:
#         return render_template("login.html")

# @app.route("/login" , methods=["POST"])
# def login_post():
#     name = request.form.get("name")
#     password = request.form.get("password")
#     conn = sqlite3.connect("task_list.db")
#     c = conn.cursor()
#     c.execute("SELECT id FROM users where name = ? AND password = ?",(name,password))
#     user_id = c.fetchone()
#     c.close()
#     if user_id is None:
#         return render_template("login.html")
#     else:
#         session["user_id"] = user_id[0]
#         return redirect("/list")

# @app.route("/logout")
# def logout():
#     session.pop("user_id",None)
#     return redirect("/login")

if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=True)