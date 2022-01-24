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
def getGameIndex(games):
    gameIndex = []

    gameSum = 0     # ゲーム数
    throwSum = 0    # 投球数
    scoreSum = 0    # 合計スコア

    # 抽出
    for game in games:
        for g in game:
            gameSum += 1
            throwSum += sum(len(s) for s in g['frameScore'])
            scoreSum += g['score']

    gameIndex.append(["ゲーム数", gameSum])
    gameIndex.append(["投球数", throwSum])
    gameIndex.append(["合計スコア", scoreSum])
    gameIndex.append(["アベレージ", float('{:.1f}'.format(scoreSum / gameSum))])
    
    return gameIndex

