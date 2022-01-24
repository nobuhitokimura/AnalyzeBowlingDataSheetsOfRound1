###
### ゲームの番号とスコアをソート（ゲーム番号順）して取得
###
def getGameNumAndTotalScores(games):
    # ゲーム番号とスコアのみを取得
    gameNumScoresDic = {}
    for game in games:
        for g in game:
            gameNumScoresDic[g['gamenum']] = g['score']

    # ソートしてゲーム番号とスコアをそれぞれ取得
    gameNum = []        # ゲーム番号
    totalScores = []    # スコア
    for gVal in sorted(gameNumScoresDic.items()):
        gameNum.append(gVal[0])
        totalScores.append(gVal[1])

    return gameNum, totalScores


###
### 1から9ピンとマークとガター、ミスの割合を取得する関数
###
#def getMarks(games):
def getMarks():
    games = [[{'1-1': 'gutter', '1-2': '5', '2-1': '8', '2-2': 'miss', '3-1': 'split 8', '3-2': '1', '4-1': 'strike', '4-2': 'none', '5-1': 'strike', '5-2': 'none', '6-1': '6', '6-2': 'miss', '7-1': '8', '7-2': '1', '8-1': '9', '8-2': 'spare', '9-1': '9', '9-2': 'miss', '10-1': 'strike', '10-2': '6', '10-3': 'spare', 'score': '127', 'gamenum': '1'}, {'1-1': '8', '1-2': 'spare', '2-1': '7', '2-2': 'spare', '3-1': '8', '3-2': 'miss', '4-1': '7', '4-2': 'spare', '5-1': '9', '5-2': 'miss', '6-1': 'strike', '6-2': 'none', '7-1': '7', '7-2': 'miss', '8-1': 'strike', '8-2': 'none', '9-1': '9', '9-2': 'spare', '10-1': '7', '10-2': '2', '10-3': 'none', 'score': '141', 'gamenum': '2'}, {'1-1': '7', '1-2': '1', '2-1': '8', '2-2': 'spare', '3-1': '8', '3-2': 'spare', '4-1': '9', '4-2': 'miss', '5-1': '9', '5-2': 'spare', '6-1': '9', '6-2': 'spare', '7-1': 'split 6', '7-2': 'miss', '8-1': 'strike', '8-2': 'none', '9-1': '9', '9-2': 'spare', '10-1': 'strike', '10-2': '9', '10-3': 'miss', 'score': '154', 'gamenum': '3'}, {'1-1': 'strike', '1-2': 'none', '2-1': '9', '2-2': 'spare', '3-1': 'strike', '3-2': 'none', '4-1': 'split 8', '4-2': '1', '5-1': 'strike', '5-2': 'none', '6-1': '6', '6-2': 'spare', '7-1': 'strike', '7-2': 'none', '8-1': 'strike', '8-2': 'none', '9-1': 'strike', '9-2': 'none', '10-1': '7', '10-2': 'spare', '10-3': '5', 'score': '200', 'gamenum': '4'}, {'1-1': 'strike', '1-2': 'none', '2-1': '9', '2-2': 'spare', '3-1': '8', '3-2': 'spare', '4-1': '8', '4-2': 'miss', '5-1': '7', '5-2': '2', '6-1': 'split 8', '6-2': '1', '7-1': '6', '7-2': 'miss', '8-1': 'strike', '8-2': 'none', '9-1': 'strike', '9-2': 'none', '10-1': '9', '10-2': 'miss', '10-3': 'none', 'score': '145', 'gamenum': '5'}, {'1-1': '8', '1-2': 'spare', '2-1': '7', '2-2': 'spare', '3-1': '8', '3-2': '1', '4-1': 'split 8', '4-2': 'miss', '5-1': '9', '5-2': 'miss', '6-1': '8', '6-2': 'miss', '7-1': '9', '7-2': 'spare', '8-1': '6', '8-2': '3', '9-1': '9', '9-2': 'spare', '10-1': '9', '10-2': 'spare', '10-3': 'strike', 'score': '133', 'gamenum': '6'}], [{'1-1': '9', '1-2': 'miss', '2-1': 'split 8', '2-2': 'spare', '3-1': 'strike', '3-2': 'none', '4-1': 'strike', '4-2': 'none', '5-1': '8', '5-2': 'spare', '6-1': '7', '6-2': 'spare', '7-1': '8', '7-2': 'spare', '8-1': 'strike', '8-2': 'none', '9-1': 'strike', '9-2': 'none', '10-1': 'strike', '10-2': '7', '10-3': 'miss', 'score': '199', 'gamenum': '10'}, {'1-1': 'strike', '1-2': 'none', '2-1': '7', '2-2': 'spare', '3-1': '8', '3-2': 'spare', '4-1': '9', '4-2': 'spare', '5-1': '7', '5-2': 'spare', '6-1': 'strike', '6-2': 'none', '7-1': '6', '7-2': '3', '8-1': '9', '8-2': 'spare', '9-1': 'split 8', '9-2': 'miss', '10-1': '8', '10-2': 'miss', '10-3': 'none', 'score': '156', 'gamenum': '11'}, {'1-1': '9', '1-2': 'miss', '2-1': '9', '2-2': 'miss', '3-1': 'split 7', '3-2': 'miss', '4-1': '8', '4-2': 'miss', '5-1': '8', '5-2': '1', '6-1': '9', '6-2': 'miss', '7-1': '9', '7-2': 'spare', '8-1': '9', '8-2': 'spare', '9-1': '9', '9-2': 'spare', '10-1': 'strike', '10-2': '9', '10-3': 'miss', 'score': '128', 'gamenum': '12'}, {'1-1': '7', '1-2': '2', '2-1': '8', '2-2': 'spare', '3-1': 'strike', '3-2': 'none', '4-1': '7', '4-2': 'spare', '5-1': 'strike', '5-2': 'none', '6-1': '7', '6-2': 'spare', '7-1': 'strike', '7-2': 'none', '8-1': '9', '8-2': 'spare', '9-1': '8', '9-2': 'spare', '10-1': '9', '10-2': 'spare', '10-3': '9', 'score': '185', 'gamenum': '7'}, {'1-1': 'strike', '1-2': 'none', '2-1': 'strike', '2-2': 'none', '3-1': '8', '3-2': 'spare', '4-1': '5', '4-2': '4', '5-1': '6', '5-2': 'spare', '6-1': '9', '6-2': 'spare', '7-1': '8', '7-2': '1', '8-1': 'split 6', '8-2': 'miss', '9-1': '7', '9-2': '1', '10-1': '8', '10-2': 'spare', '10-3': '9', 'score': '151', 'gamenum': '8'}, {'1-1': 'strike', '1-2': 'none', '2-1': 'strike', '2-2': 'none', '3-1': 'strike', '3-2': 'none', '4-1': 'strike', '4-2': 'none', '5-1': '8', '5-2': 'miss', '6-1': '9', '6-2': 'miss', '7-1': '8', '7-2': 'spare', '8-1': 'strike', '8-2': 'none', '9-1': 'strike', '9-2': 'none', '10-1': 'strike', '10-2': '9', '10-3': 'miss', 'score': '212', 'gamenum': '9'}]]

    # 辞書型で定義して0で初期化
    marksDic = {}
    marksDic["strike"] = 0
    marksDic["spare"] = 0
    for i in range(9, 0, -1):
        marksDic[str(i)] = 0
    marksDic["gutter"] = 0
    marksDic["miss"] = 0

    # 出現回数をカウント
    cnt = 0 # 投球カウント
    for game in games:
        for gDic in game:
            for gKey, gVal in gDic.items():
                # スペア
                if gVal == "spare":
                    marksDic[gVal] += 1
                    continue
                # データの合計得点scoreとゲーム数gamenum、及びnoneと2投目はカウントしない
                if gKey == "score" or gKey == "gamenum" or gVal == "none" or gKey[-1] == "2":
                    continue

                # マーク及びガターとミス
                if gVal == "strike" or gVal == "gutter" or gVal == "miss":
                    marksDic[gVal] += 1
                # それ以外
                else:
                    marksDic[gVal[-1]] += 1
            cnt += 10   # 各ゲームごとに10投分加算

    print(marksDic)
