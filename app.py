# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import fitz
import copy
import re
import numpy as np
import math
import itertools
from PIL import Image

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
    filePath = os.getcwd() + "/static/pdf/" + fileName
    # ファイルを保存する
    f.save(filePath)

    # PDFの情報抽出、画像抽出と保存
    text = getInfo(filePath)

    # PDFは不要なので削除
    os.remove(filePath)

    # 画像からゲームカウントを抽出
    game = getGameCount()

    return render_template('index.html',
        title = 'ボウリングのデータシート（ラウンドワン）',
		message = text,
        message2 = game)


###
### PDFのテキスト情報および画像を取得する関数
###
def getInfo(pdfFilePath):
    # PDfから取得した画像を格納するフォルダ
    pdfPicPath = os.getcwd() + "/static/pdfPic/"
    
    # ファイルオープン
    with fitz.open(pdfFilePath) as scoreSheet:
        # 1ページごとに解析
        for i, page in enumerate(scoreSheet):
            # テキスト情報抽出
            infoList = []   # 1PDFのテキスト情報のリスト
            infoDic = {}    # 1ゲーム分のテキスト情報の辞書型
            textNum = len(page.get_text('blocks'))  # テキスト及び画像の総数
            textCnt = 0 # 抽出した回数
            for j, text in enumerate(page.get_text('blocks')):
                if all([j!=0, j<textNum-2]):
                    # 1ゲーム分の情報を取得した場合
                    if textCnt == 3:
                        infoList.append(infoDic)
                        infoDic = {}
                        textCnt = 0
                        continue

                    textBuf = text[4]
                    # 日時
                    if textCnt == 0:
                        infoDic['year'] = textBuf[0:4]
                        infoDic['month'] = textBuf[5:7]
                        infoDic['day'] = textBuf[8:10]
                        infoDic['dow'] = textBuf[11:12]
                        infoDic['hour'] = textBuf[13:15]
                        infoDic['minute'] = textBuf[16:18]
                    # ユーザ名
                    elif textCnt == 1:
                        infoDic['username'] = textBuf.split()[0]
                    # 店名、レーン番号、ゲーム番号
                    else:
                        textSl = textBuf.splitlines()
                        infoDic['branch'] = textSl[0]
                        infoDic['lane'] = textSl[1].split("番")[0]
                        infoDic['gamenum'] = re.split('[第|ゲーム]', textSl[2])[1]

                    textCnt += 1

            # 画像取得
            for j, img in enumerate(page.get_images()):
                if j < (len(page.get_images()) - 2):
                    x = scoreSheet.extract_image(img[0])
                    picPath = os.path.join(pdfPicPath, f"{infoList[j]['gamenum']}.{x['ext']}")
                    
                    with open(picPath, "wb") as ofh:
                        ofh.write(x['image'])

            return infoList

    return -1


# 各カウントマークのPng情報
cntCharName = []       # 各マークの名前
cntCharPngDic = {}     # 各マークのPng配列
cntCharPngPath = os.getcwd() + "/static/cntCharPng"

# ゲームのpng画像があるフォルダパス
picPath = os.getcwd() + "/static/pdfPic"


###
### 各カウントマークのPng情報を読み込む関数
###
def readCntCharPng(path):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            # 名前取得
            nameBuf = file.split('.')[0]
            cntCharName.append(nameBuf)
            # Png配列取得(キーは各マークの名前)
            # pillowライブラリで読み込み、グレースケールに変化し、数値化
            charImg = np.array(Image.open(path + '/' + file).convert('L'))
            cntCharPngDic[nameBuf] = np.array(list(itertools.chain.from_iterable(charImg)))



###
### スプリットの判定(スプリット:1, それ以外:0)
###
def isSplit(threshImgCnt):
    if (sum(0==tI for tI in threshImgCnt[4,:]) + sum(0==tI for tI in threshImgCnt[31,:])) == 8:
        return 1
    return 0


###
### カウントの判定
###
def checkCount(threshImgCnt):
    # 対象のカウント画像の真ん中部分を取得
    threshImgCntBuf = np.array(list(itertools.chain.from_iterable(threshImgCnt[9:27, 8:26])))

    # 各カウント画像と比較
    result = {}
    for cntChar in cntCharName:
        result[cntChar] = sum(cntCharPngDic[cntChar]==threshImgCntBuf)
    
    # 判定結果(最大値)を返す
    maxKey, maxValue = max(result.items(), key=lambda x: x[1])
    return maxKey, maxValue


###
### 対象のゲームのPng画像のカウントを表示する関数
###
def showCount(threshImg):
    gameScore = {}
    
    for i in range(21):
        upperL = 2 + i * 35 + i * 2
        lowerR = 36 + i * 35 + i * 2 + 1
        threshImgCnt = threshImg[34:70, upperL:lowerR]
        
        # カウントの値を取得
        maxKey, maxValue = checkCount(threshImgCnt)

        # 結果表示
        if i == 20: #10フレ3投目
            if isSplit(threshImgCnt):
                gameScore['10-3'] = 'split ' + str(maxKey)
            else:
                gameScore['10-3'] = str(maxKey)
        else:
            key = str(math.floor(i/2)+1) + '-' + str(i%2+1)
            if isSplit(threshImgCnt):
                gameScore[key] = 'split ' + str(maxKey)
            else:
                gameScore[key] = str(maxKey)
    return gameScore


###
### ゲームスコアを取得する関数
###
def getGameScore(threshImg):
    # 1フレから10フレまでの各カウント
    gameCnt = []

    for i in range(21):
        upperL = 2 + i * 35 + i * 2
        lowerR = 36 + i * 35 + i * 2 + 1
        threshImgCnt = threshImg[34:70, upperL:lowerR]

        # カウントの値を取得
        maxKey, maxValue = checkCount(threshImgCnt)
        gameCnt.append(maxKey)
    
    # missとgutterを0に変換し,数字を数値に変換
    transGameCnt = [0 if (cnt == 'miss' or cnt == 'gutter') else cnt if (cnt == 'strike' or cnt == 'spare' or cnt == 'none') else int(cnt) for cnt in gameCnt]

    # スコア計算
    score = 0
    for i in range(10):
        # 10フレ
        if i == 9:
            # ストライク
            if transGameCnt[2*i] == 'strike':
                # ストライクtoストライク
                if transGameCnt[2*i+1] == 'strike':
                    # パンチアウト
                    if transGameCnt[2*i+2] == 'strike':
                        score = score + 30
                    else:
                        score = score + 20 + transGameCnt[2*i+2]
                # ストライクtoスペア
                elif transGameCnt[2*i+2] == 'spare':
                    score = score + 20
                else:
                    score = score + 10 + transGameCnt[2*i+1] + transGameCnt[2*i+2]
            # スペア
            elif transGameCnt[2*i+1] == 'spare':
                #スペアtoストライク
                if transGameCnt[2*i+2] == 'strike':
                    score = score + 20
                else:
                    score = score + 10 + transGameCnt[2*i+2]
            # その他
            else:
                score = score + transGameCnt[2*i] + transGameCnt[2*i+1]
            continue

        # ストライク
        if transGameCnt[2*i] == 'strike':
            # ダブル
            if transGameCnt[2*(i+1)] == 'strike':
                # ターキー(9フレ)
                if i == 8 and transGameCnt[2*(i+1)+1] == 'strike':
                    score = score + 30
                elif transGameCnt[2*(i+2)] == 'strike':
                    score = score + 30
                else:
                    score = score + 20 + transGameCnt[2*(i+2)]
            # ストライクtoスペア
            elif transGameCnt[2*(i+1)+1] == 'spare':
                score = score + 20
            else:
                score = score + 10 + transGameCnt[2*(i+1)] + transGameCnt[2*(i+1)+1]
        # スペア
        elif transGameCnt[2*i+1] == 'spare':
            # スペアtoストライク
            if transGameCnt[2*(i+1)] == 'strike':
                score = score + 20
            else:
                score = score + 10 + transGameCnt[2*(i+1)]
        # その他
        else:
            score = score + transGameCnt[2*i] + transGameCnt[2*i+1]
    return str(score)


def getGameCount():
    # 各マーク画像の情報を取得
    readCntCharPng(cntCharPngPath)

    # pdfPicに画像が存在するかの判定
    if os.path.isdir(picPath):
        # 画像のファイル名を取得しソート
        files = os.listdir(picPath)
        files.sort()

        gameCount = []  # ゲームカウント

        # 各ゲームの画像に対してカウントを抽出
        for file in files:
            # 各ゲームのpng画像のパスを生成
            joinPicPath = os.path.join(picPath, file)
            
            # 画像を読み込み
            img = np.array(Image.open(joinPicPath).convert('L'))
            # 二値化
            threshold = 48
            maxVal = 255            
            threshImg = np.array((img > threshold) * maxVal, dtype=np.uint8)

            # カウントを取得
            gameCountBuf = showCount(threshImg)
            # ゲームスコアを取得
            gameCountBuf['score'] = getGameScore(threshImg)
            # ゲーム数(fileの拡張子なし名)を取得
            gameCountBuf['gamenum'] = os.path.splitext(os.path.basename(file))[0]
            # ゲームカウント配列に追加
            gameCount.append(gameCountBuf)
            # 画像を削除
            os.remove(joinPicPath)
        return gameCount
    return -1


if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))