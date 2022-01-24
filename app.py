# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import getPDFInfo
import getCount
import organizeData

app = Flask(__name__)
# ファイルサイズ上限は、とりあえず10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html',
        result1 = '',
        result2 = '')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
    # ファイルリクエストのパラメータを取得
    files = request.files.getlist('pdf')

    texts = []
    games = []

    for f in files:
        # ファイル名を取得
        fileName = secure_filename(f.filename)
        # ファイルを保存するパスを指定
        filePath = BASE_PATH + "/static/pdf/" + fileName
        print("PATH ===== " + filePath )
        # ファイルを保存する
        f.save(filePath)

        # PDFの情報抽出、画像抽出
        text = getPDFInfo.getInfo(filePath)

        # PDFは不要なので削除
        os.remove(filePath)

        # 画像からゲームカウントを抽出
        game = getCount.getGameCount()

        texts.append(text)
        games.append(game)
        
    # ゲーム番号のみ取得
    #gameNum = organizeData.getGameNum(texts)
    # スコアのみ取得
    #totalScores = organizeData.getTotalScores(games)
    # ゲーム番号とスコアをソートして取得
    gameNum, totalScores = organizeData.getGameNumAndTotalScores(games)

    return render_template('index.html',
        result1 = gameNum,
        result2 = totalScores,
        all = games)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))