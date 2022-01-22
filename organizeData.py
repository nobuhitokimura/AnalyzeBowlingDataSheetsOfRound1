# ゲーム番号を取得する関数
def getGameNum(texts):
    gameNum = []
    for text in texts:
        for t in text:
            gameNum.append(t['gamenum'])

    return gameNum

# ゲームの合計点を取得する関数
def getTotalScores(games):
    totalScores = []
    for game in games:
        for g in game:
            totalScores.append(int(g['score']))

    return totalScores
