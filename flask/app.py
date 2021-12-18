# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import getPDFInfo
import getCount

app = Flask(__name__)
# ファイルサイズ上限は、とりあえず2MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html',
		title = 'ボウリングのデータシート（ラウンドワン）',
		message = 'データシートPDFを1つアップロードしてください',
        message2 = '')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
    # ファイルリクエストのパラメータを取得
    f = request.files.get('pdf')
    # ファイル名を取得
    fileName = secure_filename(f.filename)
    # ファイルを保存するパスを指定
    filePath = 'static/pdf/' + fileName
    # ファイルを保存する
    f.save(filePath)

    # PDFの情報抽出、画像抽出と保存
    text = getPDFInfo.getInfo(filePath)
    #print(text)

    # PDFは不要なので削除
    os.remove(filePath)

    # 画像からゲームカウントを抽出
    game = getCount.getGameCount()
    #print(game)

    return render_template('index.html',
        title = 'ボウリングのデータシート（ラウンドワン）',
		message = text,
        message2 = game)


if __name__ == '__main__':
	app.run(debug=True)