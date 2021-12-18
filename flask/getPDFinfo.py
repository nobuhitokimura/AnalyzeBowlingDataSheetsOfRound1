import os
import fitz
import copy
import re


###
### PDFのテキスト情報および画像を取得する関数
###
def getPDFInfo(fileName):
    # PDFのファイルパス
    pdfFilePath = "./static/pdf/" + fileName
    # PDfから取得した画像を格納するフォルダ
    pdfPicPath = "./static/pidPic"
    #os.makedirs(dirPath, exist_ok=True)

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
                    print("----------")
                    print(j, textBuf)
                    # 日時
                    if textCnt == 0:
                        infoDic["year"] = textBuf[0:4]
                        infoDic["month"] = textBuf[5:7]
                        infoDic["day"] = textBuf[8:10]
                        infoDic["dow"] = textBuf[11:12]
                        infoDic["hour"] = textBuf[13:15]
                        infoDic["minute"] = textBuf[16:18]
                    # ユーザ名
                    elif textCnt == 1:
                        infoDic["username"] = textBuf.split(' ')[0]
                    # 店名、レーン番号、ゲーム番号
                    else:
                        textSl = textBuf.splitlines()
                        infoDic["branch"] = textSl[0]
                        infoDic["lane"] = textSl[1].split("番")[0]
                        infoDic["gamenum"] = re.split('[第|ゲーム]', textSl[2])[1]

                    textCnt += 1
            
            print(infoList)

'''
            # 画像取得
            for j, img in enumerate(page.getImageList()):
                if j < (len(page.getImageList()) - 2):
                    x = scoreSheet.extractImage(img[0])
                    name = os.path.join(os.getcwd(), folderName, f"{gameNum[j]}.{x['ext']}")
                    
                    print("name : ", gameNum[j])
                    with open(name, "wb") as ofh:
                        ofh.write(x['image'])
'''



###
### 対象のPDFの日時とゲーム数の情報を取得する関数
###             
def getGameNum(page):
    gameNumBuf = []
    dateBuf = ""
    gameBuf = ""
    for text in enumerate(page.getText('blocks')):
        # 日時を取得
        if text[0] % 4 == 1 and '（' in text[1][4]:
            getDate = re.split('[/|（|）|:|\n]', text[1][4])
            dateBuf = str(getDate[0]) + "-" + str(getDate[1]) + "-" + str(getDate[2]) + "_" + str(getDate[4]) + "-" + str(getDate[5])
        
        # ゲーム数の番がある配列の最後を取得, 保存するpng名を生成
        buf = text[1][4].splitlines()
        if len(buf) == 3:
            gameBuf = str(re.split('[第|ゲーム]', buf[2])[1])
            gameNumBuf.append(dateBuf + "_" + gameBuf)
    return gameNumBuf

###
### ゲーム情報だけを取得する関数
###
def getGameInfo(page):
    for text in enumerate(page.getText('blocks')):
        buf = text[1][4].splitlines()

        if (len(buf) > 1) or ((len(text[1][4]) - len(buf[0])) > 0):
            if "Powered" not in buf[0]:
                print(buf)

# -----------------------------------------------------------------


#fileName = "score_sheet_20211218161724.pdf"
fileName = "score_sheet_20211218161746.pdf"
#fileName = "score_sheet_20211218161800.pdf"
#fileName = "score_sheet_20211218161818.pdf"
#fileName = "score_sheet_20211218161829.pdf"
getPDFInfo(fileName)
