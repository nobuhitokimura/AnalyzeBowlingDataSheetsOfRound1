import os
import fitz
import copy
import re


###
### PDFのテキスト情報および画像を取得する関数
###
def getInfo(pdfFilePath):
    # PDFのファイルパス
    #pdfFilePath = "./static/pdf/" + fileName
    # PDfから取得した画像を格納するフォルダ
    pdfPicPath = "./static/pdfPic/"
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
