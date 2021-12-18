import os
import fitz
import copy
import re


###
### PDFのテキストおよび画像を取得する関数
###
def getPDFInfo(fileName, folderName):
    # PDfから取得した画像を格納するフォルダ
    dirPath = os.path.dirname(fileName) + '/' + folderName
    os.makedirs(dirPath, exist_ok=True)

    # ファイルオープン
    with fitz.open(fileName) as scoreSheet:
        # 1ページごとに解析
        for i, page in enumerate(scoreSheet):
            # テキスト抽出
            #getGameInfo(page)
            
            # ゲーム番号取得
            gameNum = copy.copy(getGameNum(page))
            
            # 画像取得
            for j, img in enumerate(page.getImageList()):
                if j < (len(page.getImageList()) - 2):
                    x = scoreSheet.extractImage(img[0])
                    name = os.path.join(os.getcwd(), folderName, f"{gameNum[j]}.{x['ext']}")
                    
                    print("name : ", gameNum[j])
                    with open(name, "wb") as ofh:
                        ofh.write(x['image'])




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


#getPDFInfo('../pdfData/score_sheet_20210929005339.pdf', 'pic')

#dirPath = os.path.dirname(fileName) + '/' + folderName
#os.makedirs(dirPath, exist_ok=True)

fileName = "score_sheet_20211218161724.pdf"
filePath = "./static/pdf/" + fileName

# ファイルオープン
with fitz.open(filePath) as scoreSheet:
    # 1ページごとに解析
    for i, page in enumerate(scoreSheet):
        textNum = len(page.get_text('blocks'))
        for j, text in enumerate(page.get_text('blocks')):
            if all([j!=0, j<textNum-2]):
                print("----------")
                #print(text)
                print(j, text[4])
            
