# Flaskからimportしてflaskを使えるようにする
from flask import Flask,render_template,request,redirect,session
import sqlite3

#appっていう名前でFlaskアプリをつくっていくよ～みたいな
app = Flask(__name__)

#シークレットキー設定（sesionが使えるようになる！）
app.secret_key = "08smmon28"

from datetime import datetime

@app.route('/')
def concept():
    return render_template('concept.html')

@app.route('/home')
def index():
    return render_template('bbs.html')

# /page_1 と入れる page_1.htmlにとぶ
@app.route("/page_1")
def page_1():
    return render_template("page_1.html")

# /page_2 と入れる page_2.htmlにとぶ
@app.route("/page_2")
def page_2():
    return render_template("page_2.html")

# /page_3 と入れる page_3.htmlにとぶ
@app.route("/page_3")
def page_3():
    return render_template("page_3.html")

# /page_4 と入れる page_4.htmlにとぶ
@app.route("/page_4")
def page_4():
    return render_template("page_4.html")

# GET  /register => 登録画面を表示
# POST /register => 登録処理をする
@app.route('/register',methods=["GET", "POST"])
def register():
    #  登録ページを表示させる
    if request.method == "GET":
        if 'user_id' in session :
            return redirect ('/bbs')
        else:
            return render_template("register.html")

    # ここからPOSTの処理
    else:
        # 登録ページで登録ボタンを押した時に走る処理
        name = request.form.get("name")
        password = request.form.get("password")

        conn = sqlite3.connect('k_post.db')
        c = conn.cursor()
        # 課題4の答えはここ
        c.execute("insert into users values(null,?,?)", (name,password))
        conn.commit()
        conn.close()
        return redirect('/login')


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'user_id' in session :
            return redirect("/bbs")
        else:
            return render_template("login.html")
    else:
        # ブラウザから送られてきたデータを受け取る
        name = request.form.get("name")
        password = request.form.get("password")

        # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
        # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
        conn = sqlite3.connect('k_post.db')
        c = conn.cursor()
        c.execute("select id from users where name = ? and password = ?", (name, password) )
        user_id = c.fetchone()
        conn.close()
        # DBから取得してきたuser_id、ここの時点ではタプル型
        print(type(user_id))
        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if user_id is None:
            # ログイン失敗すると、ログイン画面に戻す
            return render_template("login.html")
        else:
            session['user_id'] = user_id[0]
            return redirect("/bbs")


@app.route("/logout")
def logout():
    session.pop('user_id',None)
    # ログアウト後はログインページにリダイレクトさせる
    return redirect("/login")


@app.route('/bbs')
def bbs():
    if 'user_id' in session :
        user_id = session['user_id']
        conn = sqlite3.connect('k_post.db')
        c = conn.cursor()
        # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
        # クッキーから取得したuser_idを使用してusersテーブルのnameを取得
        c.execute("select name from users where id = ?", (user_id,))
        # fetchoneはタプル型
        user_info = c.fetchone()
        # user_infoの中身を確認

        # 課題1の答えはここ del_flagが0のものだけ表示する
        # 課題2の答えはここ 保存されているtimeも表示する
        c.execute("select id,comment,time from k_posts where user_id = ? and del_flag = 0 order by id", (user_id,))
        comment_list = []
        for row in c.fetchall():
            comment_list.append({"id": row[0], "comment": row[1], "time":row[2]})

        c.close()
        return render_template('bbs.html' , user_info = user_info , comment_list = comment_list)
    else:
        return redirect("/login")


@app.route('/add', methods=["POST"])
def add():
    user_id = session['user_id']
    # 現在時刻を取得
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    # POSTアクセスならDBに登録する
    # フォームから入力されたアイテム名の取得
    comment = request.form.get("comment")
     # チェックボックスから選択されたカテゴリーの取得
    cat_id = request.form.get("cat_id") 
    conn = sqlite3.connect('k_post.db')
    c = conn.cursor()
    # 現在の最大ID取得(fetchoneの戻り値はタプル)

    # null,?,?,0の0はdel_flagのデフォルト値
    # cat_idを新たにinsert
    c.execute("insert into k_posts values(null,?,?,0,?,?)", (user_id, comment,time,cat_id))
    conn.commit()
    conn.close()
    return redirect('/bbs')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' in session :
        conn = sqlite3.connect('k_post.db')
        c = conn.cursor()
        c.execute("select comment from k_posts where id = ?", (id,) )
        comment = c.fetchone()
        conn.close()

        if comment is not None:
            # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
            comment = comment[0] # "りんご" ○   ("りんご",) ☓
            # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
        else:
            return "アイテムがありません" # 指定したIDの name がなければときの対処

        item = { "id":id, "comment":comment }

        return render_template("edit.html", comment=item)
    else:
        return redirect("/login")


# /add ではPOSTを使ったので /edit ではあえてGETを使う
@app.route("/edit")
def update_item():
    if 'user_id' in session :
        # ブラウザから送られてきたデータを取得
        item_id = request.args.get("item_id") # id
        print(item_id)
        item_id = int(item_id) # ブラウザから送られてきたのは文字列なので整数に変換する
        comment = request.args.get("comment") # 編集されたテキストを取得する

        # 既にあるデータベースのデータを送られてきたデータに更新
        conn = sqlite3.connect('k_post.db')
        c = conn.cursor()
        c.execute("update k_posts set comment = ? where id = ?",(comment,item_id))
        conn.commit()
        conn.close()

        # アイテム一覧へリダイレクトさせる
        return redirect("/bbs")
    else:
        return redirect("/login")

@app.route('/del' , methods=["POST"])
def del_task():
    id = request.form.get("comment_id")
    id = int(id)
    conn = sqlite3.connect('k_post.db')
    c = conn.cursor()
    # 指定されたitem_idを元にDBデータを削除せずにdel_flagを1にして一覧からは表示しないようにする
    # 課題1の答えはここ del_flagを1にupdateする
    c.execute("update k_posts set del_flag = 1 where id=?", (id,))
    conn.commit()
    conn.close()
    # 処理終了後に一覧画面に戻す
    return redirect("/bbs")

@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@app.errorhandler(404)
def notfound(code):
    return "sorry... 404"

if __name__ == "__main__":
    # Flask が持っている開発用サーバーを、実行します。
    app.run(debug=True)