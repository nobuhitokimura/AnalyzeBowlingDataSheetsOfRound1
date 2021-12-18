# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
# ファイルサイズ上限は、とりあえず2MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html',
		title = 'ボウリングのデータシート（ラウンドワン）',
		message = 'データシートPDFを1つアップロードしてください')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
    # ファイルリクエストのパラメータを取得
    f = request.files.get('pdf')
    # ファイル名を取得
    filename = secure_filename(f.filename)
    # ファイルを保存するパスを指定
    filepath = 'static/pdf/' + filename
    # ファイルを保存する
    f.save(filepath)

    return render_template('index.html',
        title = 'ボウリングのデータシート（ラウンドワン）',
		message = 'アップロードが完了しました')


if __name__ == '__main__':
	app.run(debug=True)