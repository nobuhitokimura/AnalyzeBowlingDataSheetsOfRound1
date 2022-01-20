import os
import numpy as np
import math
import itertools
from PIL import Image

# 各カウントマークのPng情報
cntCharName = []       # 各マークの名前
cntCharPngDic = {}     # 各マークのPng配列
cntCharPngPath = "./static/cntCharPng"

# ゲームのpng画像があるフォルダパス
picPath = "./static/pdfPic"


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
    #print(transGameCnt)

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
    #print("score : " + str(score))
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
