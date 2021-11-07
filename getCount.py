import os
import cv2
import numpy as np
import math
import itertools


# 各カウントマークのPng情報
cntCharName = []       # 各マークの名前
cntCharPngDic = {}     # 各マークのPng配列
cntCharPngPath = "./cntCharPng"

# ゲームのpng画像があるフォルダパス
picPath = "./pic"


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
            charImg = cv2.imread(path + '/' + file, 0)
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
    for i in range(21):
        upperL = 2 + i * 35 + i * 2
        lowerR = 36 + i * 35 + i * 2 + 1
        threshImgCnt = threshImg[34:70, upperL:lowerR]
        
        # カウントの値を取得
        maxKey, maxValue = checkCount(threshImgCnt)

        # 結果表示
        if i == 20:
            print("10-3 : ", end='')
        else:
            print(str(math.floor(i/2)+1) + '-' + str(i%2+1) + " : ", end='')

        if isSplit(threshImgCnt):
            print("split " + str(maxKey))
        else:
            print(str(maxKey))


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
                # ターキー
                if transGameCnt[2*(i+2)] == 'strike':
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
    
    print("score : " + str(score))

# 各マーク画像の情報を取得
readCntCharPng(cntCharPngPath)

if os.path.isdir(picPath):
    files = os.listdir(picPath)
    for file in files:
        # 各ゲームのpng画像のパスを生成
        joinPicPath = os.path.join(picPath, file)
        
        # 画像を読み込み
        img = cv2.imread(joinPicPath, 0)
        # 二値化
        threshold = 48
        ret, threshImg = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        
        # カウントを表示
        print(joinPicPath)
        #showCount(threshImg)

        # ゲームスコアを表示
        getGameScore(threshImg)
