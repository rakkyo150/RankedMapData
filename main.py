import pandas as pd
import requests

beatSaberAccessCount = 0
previousHashList = []

idList = []
leaderboardIdList = []
hashList = []
nameList = []
descriptionList = []
uploaderIdList = []
uploaderNameList = []
uploaderHashList = []
uploaderAvatarList = []
uploaderLoginTypeList = []
uploaderCuratorList = []
bpmList = []
# 曲全体の長さ
durationList = []
songAuthorNameList = []
levelAuthorNameList = []
upvotesList = []
downvotesList = []
upvotesRatioList = []
# 初回アップロード
uploadedAtList = []
# 初回マップ作成
createdAtList = []
# 最新マップ関連情報アップデート
updatedAtList = []
# マップ内容アップデート
lastPublishedAtList = []
automapperList = []
qualifiedList = []
difficultyList = []
sageScoreList = []
njsList = []
offsetList = []
notesList = []
bombsList = []
obstaclesList = []
npsList = []
# beat換算っぽい
lengthList = []
characteristicList = []
eventsList = []
chromaList = []
meList = []
neList = []
cinemaList = []
secondsList = []
errorsList = []
warnsList = []
resetsList = []
starsList = []
maxScoreList = []
downloadUrlList = []
coverUrlList = []
previewUrlList = []
tagsList = []

"""
# For local run to update all, change "00" to now hour
if datetime.datetime.now().strftime("%H")=="00":
    print("全更新")
    # 空のDataframe
    previousDf = pd.DataFrame(columns=["id","leaderboardId","hash","name","bpm","duration","songAuthorName","levelAuthorName",
                             "upvotesRatio","uploadedAt","automapper","difficulty","createdAt","sageScore",
                             "njs","offset","notes","bombs","obstacles","nps","length","characteristic",
                             "events","chroma","me","ne","cinema","seconds","errors","warns","resets","stars"],
                              index=[])
    previousHashList = []
else:
    print("追加譜面分更新")
    githubEndpoint="https://api.github.com/repos/rakkyo150/RankedMapData/releases/latest"
    headers={'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'}
    githubResponse=requests.get(url=githubEndpoint,headers=headers)
    releaseJson=githubResponse.json()
    secondHeaders={'Accept': 'application/octet-stream' }
    csvResponse=requests.get(url=releaseJson["assets"][0]["browser_download_url"],headers=secondHeaders)
    previousDf = pd.read_csv(io.BytesIO(csvResponse.content),sep=",",index_col=0,encoding="utf-8")
    previousHashListTemp = previousDf["hash"].to_list()
    for item in previousHashListTemp:
        # のちの比較のために大文字化しておく
        previousHashList.append(item.upper())
"""

print("全更新")
# 空のDataframe
previousDf = pd.DataFrame(
    columns=["id", "leaderboardId", "hash", "name", "description", "uploaderId",
             "uploaderName", "uploaderHash", "uploaderAvatar", "uploaderLoginType",
             "uploaderCurator", "bpm", "duration", "songAuthorName", "levelAuthorName",
             "upvotes", "downvotes", "upvotesRatio", "uploadedAt", "createdAt", "updatedAt",
             "lastPublishedAt", "automapper", "qualified", "difficulty", "sageScore",
             "njs", "offset", "notes", "bombs", "obstacles", "nps", "length", "characteristic",
             "events", "chroma", "me", "ne", "cinema", "seconds", "errors", "warns", "resets",
             "stars",
             "maxScore", "downloadUrl", "coverUrl", "previewUrl", "tags"],
    index=[])
previousHashList = []

pageNumber = 0
while True:
    pageNumber += 1
    # ランク譜面の情報を最新のものから順に
    scoreSaberResponse = requests.get(
        f"https://scoresaber.com/api/leaderboards?ranked=true&category=1&sort=0&page={pageNumber}")
    jsonData = scoreSaberResponse.json()
    if len(jsonData["leaderboards"]) == 0:
        break
    for j in jsonData["leaderboards"]:
        # 更新分だけ取得したので終了
        # 小文字だけのハッシュや大文字小文字両方のハッシュが存在する譜面の対応のため、比較するときは大文字にそろえる
        # 一度ハッシュを取得すれば他難易度の同ハッシュは重複するのでいらない
        if j["songHash"].upper() in previousHashList:
            pass
        else:
            beatSaberAccessCount += 1
            print(f"{beatSaberAccessCount}回目の取得")
            print(j["songName"])
            previousHashList.append(j["songHash"].upper())
            # ハッシュが一致する譜面の全難易度の情報を取得していく
            beatSaverResponse = requests.get(f'https://api.beatsaver.com/maps/hash/{j["songHash"]}')

            # ScoreSaberに情報はあるけどBeatSaverでは消されたっぽい譜面
            if beatSaverResponse.status_code == 404:
                print(
                    f"{beatSaverResponse.status_code} Not Found: {j['songName']}-{j['id']}-{j['songHash']}")
                pass

            else:
                mapDetail = beatSaverResponse.json()
                mapDifficulty = mapDetail["versions"][-1]["diffs"]

                for k in mapDifficulty:

                    if "stars" in k:
                        idList += [mapDetail["id"]]
                        leaderboardIdList += [j["id"]]
                        hashList += [j["songHash"]]
                        nameList += [mapDetail["name"]]
                        descriptionList += [mapDetail["description"]]
                        uploaderIdList += [mapDetail["uploader"]["id"]]
                        uploaderNameList += [mapDetail["uploader"]["name"]]
                        uploaderHashList += [mapDetail["uploader"]["hash"]]
                        uploaderAvatarList += [mapDetail["uploader"]["avatar"]]
                        uploaderLoginTypeList += [mapDetail["uploader"]["type"]]
                        uploaderCuratorList += [mapDetail["uploader"]["curator"]]
                        bpmList += [mapDetail["metadata"]["bpm"]]
                        durationList += [mapDetail["metadata"]["duration"]]
                        songAuthorNameList += [mapDetail["metadata"]["songAuthorName"]]
                        levelAuthorNameList += [mapDetail["metadata"]["levelAuthorName"]]
                        upvotesList += [mapDetail["stats"]["upvotes"]]
                        downvotesList += [mapDetail["stats"]["downvotes"]]
                        upvotesRatioList += [mapDetail["stats"]["score"]]
                        uploadedAtList += [mapDetail["uploaded"]]
                        createdAtList += [mapDetail["createdAt"]]
                        updatedAtList += [mapDetail["updatedAt"]]
                        lastPublishedAtList += [mapDetail["lastPublishedAt"]]
                        automapperList += [mapDetail["automapper"]]
                        qualifiedList += [mapDetail["qualified"]]
                        if "sageScore" in mapDetail["versions"][-1]:
                            sageScoreList += [mapDetail["versions"][-1]["sageScore"]]
                        else:
                            sageScoreList += [None]
                        difficultyList += [k["difficulty"]]
                        njsList += [k["njs"]]
                        offsetList += [k["offset"]]
                        notesList += [k["notes"]]
                        bombsList += [k["bombs"]]
                        obstaclesList += [k["obstacles"]]
                        npsList += [k["nps"]]
                        lengthList += [k["length"]]
                        characteristicList += [k["characteristic"]]
                        eventsList += [k["events"]]
                        chromaList += [k["chroma"]]
                        meList += [k["me"]]
                        neList += [k["ne"]]
                        cinemaList += [k["cinema"]]
                        secondsList += [k["seconds"]]
                        errorsList += [k["paritySummary"]["errors"]]
                        warnsList += [k["paritySummary"]["warns"]]
                        resetsList += [k["paritySummary"]["resets"]]
                        starsList += [k["stars"]]
                        maxScoreList += [k["maxScore"]]
                        downloadUrlList += [mapDetail["versions"][-1]["downloadURL"]]
                        coverUrlList += [mapDetail["versions"][-1]["coverURL"]]
                        previewUrlList += [mapDetail["versions"][-1]["previewURL"]]
                        tagStr = ""
                        if "tags" in mapDetail:
                            for tag in mapDetail["tags"]:
                                tagStr += tag + ","
                            tagStr = tagStr[:-1]
                        else:
                            tagStr = None
                        tagsList += [tagStr]

if len(idList) == 0:
    nextDf = previousDf

else:
    # DBと同じ考え方でOK
    df = pd.DataFrame(columns=["id", "leaderboardId", "hash", "name", "description", "uploaderId",
                               "uploaderName", "uploaderHash", "uploaderAvatar",
                               "uploaderLoginType",
                               "uploaderCurator", "bpm", "duration", "songAuthorName",
                               "levelAuthorName",
                               "upvotes", "downvotes", "upvotesRatio", "uploadedAt", "createdAt",
                               "updatedAt",
                               "lastPublishedAt", "automapper", "qualified", "difficulty",
                               "sageScore",
                               "njs", "offset", "notes", "bombs", "obstacles", "nps", "length",
                               "characteristic",
                               "events", "chroma", "me", "ne", "cinema", "seconds", "errors",
                               "warns", "resets", "stars",
                               "maxScore", "downloadUrl", "coverUrl", "previewUrl", "tags"],
                      data={"id": idList, "leaderboardId": leaderboardIdList, "hash": hashList,
                            "name": nameList,
                            "description": descriptionList, "uploaderId": uploaderIdList,
                            "uploaderName": uploaderNameList,
                            "uploaderHash": uploaderHashList, "uploaderAvatar": uploaderAvatarList,
                            "uploaderLoginType": uploaderLoginTypeList,
                            "uploaderCurator": uploaderCuratorList,
                            "bpm": bpmList, "duration": durationList,
                            "songAuthorName": songAuthorNameList,
                            "levelAuthorName": levelAuthorNameList, "upvotes": upvotesList,
                            "downvotes": downvotesList,
                            "upvotesRatio": upvotesRatioList, "uploadedAt": uploadedAtList,
                            "createdAt": createdAtList,
                            "updatedAt": updatedAtList, "lastPublishedAt": lastPublishedAtList,
                            "automapper": automapperList,
                            "qualified": qualifiedList, "difficulty": difficultyList,
                            "sageScore": sageScoreList, "njs": njsList, "offset": offsetList,
                            "notes": notesList, "bombs": bombsList, "obstacles": obstaclesList,
                            "nps": npsList,
                            "length": lengthList, "characteristic": characteristicList,
                            "events": eventsList,
                            "chroma": chromaList, "me": meList, "ne": neList, "cinema": cinemaList,
                            "seconds": secondsList,
                            "errors": errorsList, "warns": warnsList, "resets": resetsList,
                            "stars": starsList,
                            "maxScore": maxScoreList, "downloadUrl": downvotesList,
                            "coverUrl": coverUrlList,
                            "previewUrl": previewUrlList, "tags": tagsList})

    print(df.head())

    nextDf = df.append(previousDf, ignore_index=True)

# For local update, change "out" to "."
# 余分な空行が入るのでnewline設定で回避
with open(f'out/outcome.csv', 'w', encoding="utf-8", newline="\n", errors="ignore") as f:
    nextDf.to_csv(f)
