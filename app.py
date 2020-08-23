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
    return render_template('index.html')

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

@app.route('/add', methods=["POST"])
def add():
    user_id = session['user_id']
    # 現在時刻を取得
    time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    # POSTアクセスならDBに登録する
    # フォームから入力されたアイテム名の取得
    content = request.form.get("content")
    conn = sqlite3.connect('k_post.db')
    c = conn.cursor()
    # 現在の最大ID取得(fetchoneの戻り値はタプル)

    # null,?,?,0の0はdel_flagのデフォルト値
    # timeを新たにinsert
    c.execute("insert into k_posts values(null,?,?,0,?)", (user_id, content,time))
    conn.commit()
    conn.close()
    return redirect('/bbs')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' in session :
        conn = sqlite3.connect('k_post.db')
        c = conn.cursor()
        c.execute("select content from k_posts where id = ?", (id,) )
        content = c.fetchone()
        conn.close()

        if content is not None:
            # None に対しては インデクス指定できないので None 判定した後にインデックスを指定
            content = contentt[0] # "りんご" ○   ("りんご",) ☓
            # fetchone()で取り出したtupleに 0 を指定することで テキストだけをとりだす
        else:
            return "アイテムがありません" # 指定したIDの name がなければときの対処

        item = { "id":id, "content":content }

        return render_template("edit.html", content=item)
    else:
        return redirect("/home")


# /add ではPOSTを使ったので /edit ではあえてGETを使う
@app.route("/edit")
def update_item():
    if 'user_id' in session :
        # ブラウザから送られてきたデータを取得
        item_id = request.args.get("item_id") # id
        print(item_id)
        item_id = int(item_id) # ブラウザから送られてきたのは文字列なので整数に変換する
        content = request.args.get("content") # 編集されたテキストを取得する

        # 既にあるデータベースのデータを送られてきたデータに更新
        conn = sqlite3.connect('k_post.db')
        c = conn.cursor()
        c.execute("update k_posts set content = ? where id = ?",(content,item_id))
        conn.commit()
        conn.close()

        # アイテム一覧へリダイレクトさせる
        return redirect("/bbs")
    else:
        return redirect("/home")

@app.route('/del' , methods=["POST"])
def del_task():
    id = request.form.get("content_id")
    id = int(id)
    conn = sqlite3.connect('k_post.db')
    c = conn.cursor()
    # 指定されたitem_idを元にDBデータを削除せずにdel_flagを1にして一覧からは表示しないようにする
    # 課題1の答えはここ del_flagを1にupdateする
    c.execute("update bbs set del_flag = 1 where id=?", (id,))
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