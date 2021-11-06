import os
import cv2
import numpy as np
import math
import itertools


# 各カウントマークのPng情報
cntCharName = []       # 各マークの名前
cntCharPngDic = {}     # 各マークのPng配列
cntCharPngPath = "./cntCharPng"


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



img = cv2.imread('./pdfData/pic/2021-9-25_11-57_4.png', 0)
threshold = 48
ret, threshImg = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
cv2.imwrite('./threshImg.png', threshImg)

readCntCharPng(cntCharPngPath)

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
