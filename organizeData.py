import copy

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
### ゲームのマーク数およびオープンフレームを取得する
###
def getMarkAndOpenflame(frameScore):
    tarFrameScore = copy.copy(frameScore)

    strikeRate = [0, 0]     # ストライク
    spareRate = [0, 0]      # スペア
    openflameRate = [0, 0]  # オープンフレーム

    while len(tarFrameScore) > 0:
        # 後ろのフレームから計算
        frame = tarFrameScore.pop(-1) # 最後のフレームを取り出し
        score = sum(frame)
        # 10フレでパンチアウト
        if score == 30:
            strikeRate[0] += 3
            strikeRate[1] += 3
        # 10フレ3投
        elif len(frame) == 3:
            # ダブル
            if frame[0] == 10 and frame[1] == 10:
                strikeRate[0] += 2
                strikeRate[1] += 3
            # ストライクとスペア（順不同）
            elif score == 20:
                strikeRate[0] += 1
                strikeRate[1] += 2
                spareRate[0] += 1
                spareRate[1] += 1
            # スペア1つのみ
            elif frame[0] + frame[1] == 10 and frame[0] != 10:
                strikeRate[1] += 2
                spareRate[0] += 1
                spareRate[1] += 1
            # 1投目ストライクだがその後オープンフレーム
            else:
                strikeRate[0] += 1
                strikeRate[1] += 2
                spareRate[1] += 1
                openflameRate[0] += 1
        # その他（10フレノーマークも含む）
        # ストライク
        elif len(frame) == 1:
            strikeRate[0] += 1
            strikeRate[1] += 1
        # スペア
        elif score == 10:
            strikeRate[1] += 1
            spareRate[0] += 1
            spareRate[1] += 1
        # オープンフレーム
        else:
            strikeRate[1] += 1
            spareRate[1] += 1
            openflameRate[0] += 1
        # オープンフレームの分母をインクリメント
        openflameRate[1] += 1
    return [strikeRate, spareRate, openflameRate]

###
### 1から9ピンとマークとガター、ミスの割合を取得する関数
###
def getGameIndex(games):
    gameIndex = []

    gameSum = 0             # ゲーム数
    throwSum = 0            # 投球数
    scoreSum = 0            # 合計スコア
    highScore = 0           # ハイスコア
    strikeRate = [0, 0]     # ストライク
    spareRate = [0, 0]      # スペア
    openflameRate = [0, 0]  # オープンフレーム
    gutterNum = 0           # ガター

    # 抽出
    for game in games:
        for g in game:
            # ゲーム数カウント
            gameSum += 1
            # 投球数を加算
            throwSum += sum(len(s) for s in g['frameScore'])
            # ゲームスコアを加算し、ハイスコアなら記録
            scoreBuf = g['score']
            scoreSum += scoreBuf
            highScore = scoreBuf if scoreBuf > highScore else highScore
            # マークおよびオープンフレーム
            markAndOpenflame = getMarkAndOpenflame(g['frameScore'])
            strikeRate = [x + y for (x, y) in zip(strikeRate, markAndOpenflame[0])]
            spareRate = [x + y for (x, y) in zip(spareRate, markAndOpenflame[1])]
            openflameRate = [x + y for (x, y) in zip(openflameRate, markAndOpenflame[2])]

    gameIndex.append(["ゲーム数", gameSum])
    gameIndex.append(["投球数", throwSum])
    gameIndex.append(["合計スコア", scoreSum])
    gameIndex.append(["ハイスコア", highScore])
    gameIndex.append(["アベレージ", float('{:.2f}'.format(scoreSum / gameSum))])
    gameIndex.append(["ストライク率（％）", float('{:.2f}'.format(strikeRate[0] / strikeRate[1] * 100))])
    gameIndex.append(["スペア率（％）", float('{:.2f}'.format(spareRate[0] / spareRate[1] * 100))])
    gameIndex.append(["オープンフレーム率（％）", float('{:.2f}'.format(openflameRate[0] / openflameRate[1] * 100))])
    
    return gameIndex

