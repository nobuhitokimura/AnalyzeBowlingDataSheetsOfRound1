import os
import fitz

def getPDFtexts(fileName, folderName):
    # PDfから取得した画像を格納するフォルダ
    dirPath = os.path.dirname(fileName) + '/' + folderName
    os.makedirs(dirPath, exist_ok=True)

    # ファイルオープン
    with fitz.open(fileName) as scoreSheet:
        # 1ページごとに解析
        for i, page in enumerate(scoreSheet):
            # 画像取得
            for j, img in enumerate(page.getImageList()):
                x = scoreSheet.extractImage(img[0])
                name = os.path.join(dirPath, f"{i:04}_{j:02}.{x['ext']}")
                with open(name, "wb") as ofh:
                    ofh.write(x['image'])
            
            # テキスト抽出
            for l, text in enumerate(page.getText('blocks')):
                print(text)


    

if __name__ == "__main__":
    getPDFtexts('./pdfData/score_sheet_20210929005339.pdf', 'pic')
    #getPDFtexts('./pdfData/score_sheet_20210929005432.pdf')

'''
    dstdir = os.path.splitext(fname)[0]
    print("dstdir:", dstdir)

    os.makedirs(dstdir, exist_ok=True)
    with fitz.open(fname) as doc:
        for i, page in enumerate(doc):
            for j, img in enumerate(page.getImageList()):
                x = doc.extractImage(img[0])
                name = os.path.join(dstdir, f"{i:04}_{j:02}.{x['ext']}")
                with open(name, "wb") as ofh:
                    ofh.write(x['image'])
'''