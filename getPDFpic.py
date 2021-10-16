import os
import fitz
import copy


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
                    name = os.path.join(dirPath, f"{gameNum[j]}.{x['ext']}")
                    with open(name, "wb") as ofh:
                        ofh.write(x['image'])




###
### 対象のPDFのゲーム数の情報を取得する関数
###             
def getGameNum(page):
    gameNumBuf = []
    for text in enumerate(page.getText('blocks')):
        buf = text[1][4].splitlines()
        # ゲーム数の番がある配列の最後を取得
        if len(buf) == 3:
            gameNumBuf.append(buf[2])
    # print("gameNumBuf:", gameNumBuf)
    return gameNumBuf

###
### ゲーム情報だけを取得する関数
###
def getGameInfo(page):
    for text in enumerate(page.getText('blocks')):
        buf = text[1][4].splitlines()
        #print('---')
        #print('文字数:{}, {}'.format(len(text[1][4]), text[1][4]))
        #print('文字数:{}, {}'.format(len(buf[0]), buf[0]))

        if (len(buf) > 1) or ((len(text[1][4]) - len(buf[0])) > 0):
            if "Powered" not in buf[0]:
                print(buf)

# -----------------------------------------------------------------

getPDFInfo('./pdfData/score_sheet_20210929005339.pdf', 'pic')
#getPDFInfo('./pdfData/score_sheet_20210929005432.pdf')