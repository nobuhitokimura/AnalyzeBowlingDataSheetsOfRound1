import os
import numpy as np
import math
import copy
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
### ゲームの合計スコアを取得する関数
###
def getTotalScore(frameScore):
    tarFrameScore = copy.copy(frameScore)

    totalScore = 0  # 合計点
    score, next1, next2 = 0, 0, 0   # フレームの合計点、1投先の倒した本数、2投先の倒した本数
    while len(tarFrameScore) > 0:
        # 後ろのフレームから計算
        frame = tarFrameScore.pop(-1) # 最後のフレームを取り出し
        score = sum(frame)
        # 10フレでパンチアウト、ストライク、スペア
        if len(frame) == 3:
            totalScore += score
            next1 = frame[0]
            next2 = frame[1]
        # ストライク
        elif len(frame) == 1:
            totalScore += 10 + next1 + next2
            next2 = next1
            next1 = 10
        # スペア
        elif score == 10:
            totalScore += 10 + next1
            next1 = frame[0]
            next2 = frame[1]
        # その他は倒した本数
        else:
            totalScore += score
            next1 = frame[0]
            next2 = frame[1]
    return totalScore


###
### フレームと投目の結果のリストを倒した本数の配列に変換する関数
###
def toFrameScore(gameCountDic):
    frameScore = []
    scoreBuf = []

    for cKey, cVal in gameCountDic.items():
        print(cKey, cVal)
        # 10フレームのみ別の処理
        if cKey[1] == '0':
            # 1投目
            if cKey[-1] == '1':
                # ストライク
                if cVal == 'strike':
                    scoreBuf.append(10)
                # ガター
                elif cVal == 'gutter':
                    scoreBuf.append(0)
                # その他は倒した本数(split用に-1番目を参照)
                else:
                    scoreBuf.append(int(cVal[-1]))
            # 2, 3投目
            else:
                # ストライク
                if cVal == 'strike':
                    scoreBuf.append(10)
                # スペア(2, 3投目それぞれで参照する配列が1つずれるため)
                elif cVal == 'spare':
                    scoreBuf.append(10 - scoreBuf[int(cKey[-1]) - 2])
                # ミス
                elif cVal == 'miss':
                    scoreBuf.append(0)
                # ガター
                elif cVal == 'gutter':
                    scoreBuf.append(0)
                # noneの場合は何もしない
                elif cVal == 'none':
                    pass
                # その他は倒した本数(split用に-1番目を参照)
                else:
                    scoreBuf.append(int(cVal[-1]))
    
                # 3投目(投げてない時も含める)
                if cKey[-1] == '3':
                    frameScore.append(scoreBuf)
                    scoreBuf = []

        else:
            # 1投目
            if cKey[-1] == '1':
                # ストライク
                if cVal == 'strike':
                    scoreBuf.append(10)
                # ガター
                elif cVal == 'gutter':
                    scoreBuf.append(0)
                # その他は倒した本数(split用に-1番目を参照)
                else:
                    scoreBuf.append(int(cVal[-1]))
            # 2投目
            else:
                # 1投目がストライクの場合
                if scoreBuf[0] == 10:
                    pass    
                # スペアを取った場合
                elif cVal == 'spare':
                    scoreBuf.append(10 - scoreBuf[0])
                # missの場合
                elif cVal == 'miss':
                    scoreBuf.append(0)
                # その他は倒した本数
                else:
                    scoreBuf.append(int(cVal))

                frameScore.append(scoreBuf)
                scoreBuf = []
    return frameScore


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

            # 各フレームのカウントを取得
            gameCountBuf = {}
            gameCountDic = showCount(threshImg)
            gameCountBuf['frameInfo'] = gameCountDic
            # 各フレームのカウントを倒したピンに変換
            gameCountBuf['frameScore'] = toFrameScore(gameCountDic)
            # ゲームスコアを取得
            gameCountBuf['score'] = getTotalScore(gameCountBuf['frameScore'])
            # ゲーム数(fileの拡張子なし名)を取得
            gameCountBuf['gamenum'] = int(os.path.splitext(os.path.basename(file))[0])
            # ゲームカウント配列に追加
            gameCount.append(gameCountBuf)
            # 画像を削除
            os.remove(joinPicPath)
        return gameCount
    return -1

