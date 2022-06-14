import pandas as pd
import requests

getDataFromBeatSaverCount = 0
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

pageNumber = 0
while True:
    pageNumber += 1
    # ランク譜面の情報を最新のものから順に
    scoreSaberResponse = requests.get(
        f"https://scoresaber.com/api/leaderboards?ranked=true&category=1&sort=0&page={pageNumber}")
    scoreSaberJsonData = scoreSaberResponse.json()
    if len(scoreSaberJsonData.get("leaderboards")) == 0:
        break
    for scoreSaberDataPerDifficulty in scoreSaberJsonData.get("leaderboards"):
        # 更新分だけ取得したので終了
        # 小文字だけのハッシュや大文字小文字両方のハッシュが存在する譜面の対応のため、比較するときは大文字にそろえる
        # 一度ハッシュを取得すれば他難易度の同ハッシュは重複するのでいらない
        if scoreSaberDataPerDifficulty.get("songHash").upper() in previousHashList:
            pass
        else:
            getDataFromBeatSaverCount += 1
            print(f"{getDataFromBeatSaverCount}回目の取得")
            print(scoreSaberDataPerDifficulty.get("songName"))
            previousHashList.append(scoreSaberDataPerDifficulty.get("songHash").upper())
            # ハッシュが一致する譜面の全難易度の情報を取得していく
            beatSaverResponse = requests.get(
                f'https://api.beatsaver.com/maps/hash/{scoreSaberDataPerDifficulty.get("songHash")}')

            # ScoreSaberに情報はあるけどBeatSaverでは消されたっぽい譜面
            if beatSaverResponse.status_code == 404:
                print(
                    f"{beatSaverResponse.status_code} Not Found: {scoreSaberDataPerDifficulty.get('songName')}-{scoreSaberDataPerDifficulty.get('id')}-{scoreSaberDataPerDifficulty.get('songHash')}")
                pass

            else:
                mapDetail = beatSaverResponse.json()
                mapDifficulty = mapDetail.get("versions")[-1].get("diffs")

                for beatSaverDataPerDifficulty in mapDifficulty:

                    # 以下BeatSaverでランク情報が抜けてたものたち
                    # The Pretender
                    # Valley of Voices
                    # All My Love
                    if ("stars" in beatSaverDataPerDifficulty) or \
                            (scoreSaberDataPerDifficulty.get(
                                "songHash").upper() == "5536BE9C26867AB38524FA53E30FC1AB889D3251" or \
                             scoreSaberDataPerDifficulty.get(
                                 "songHash").upper() == "FFEEC65EFC5212B770D6DEED6F9AD766914D7635" or \
                             scoreSaberDataPerDifficulty.get(
                                 "songHash").upper() == "7B4445883E395FFEFC41BADCE1FA3159FADA9E3C"):
                        idList += [mapDetail.get("id")]
                        leaderboardIdList += [scoreSaberDataPerDifficulty.get("id")]
                        hashList += [scoreSaberDataPerDifficulty.get("songHash")]
                        nameList += [mapDetail.get("name")]
                        descriptionList += [mapDetail.get("description")]
                        uploaderIdList += [mapDetail.get("uploader").get("id")]
                        uploaderNameList += [mapDetail.get("uploader").get("name")]
                        uploaderHashList += [mapDetail.get("uploader").get("hash")]
                        uploaderAvatarList += [mapDetail.get("uploader").get("avatar")]
                        uploaderLoginTypeList += [mapDetail.get("uploader").get("type")]
                        uploaderCuratorList += [mapDetail.get("uploader").get("curator")]
                        bpmList += [mapDetail.get("metadata").get("bpm")]
                        durationList += [mapDetail.get("metadata").get("duration")]
                        songAuthorNameList += [mapDetail.get("metadata").get("songAuthorName")]
                        levelAuthorNameList += [mapDetail.get("metadata").get("levelAuthorName")]
                        upvotesList += [mapDetail.get("stats").get("upvotes")]
                        downvotesList += [mapDetail.get("stats").get("downvotes")]
                        upvotesRatioList += [mapDetail.get("stats").get("score")]
                        uploadedAtList += [mapDetail.get("uploaded")]
                        createdAtList += [mapDetail.get("createdAt")]
                        updatedAtList += [mapDetail.get("updatedAt")]
                        lastPublishedAtList += [mapDetail.get("lastPublishedAt")]
                        automapperList += [mapDetail.get("automapper")]
                        qualifiedList += [mapDetail.get("qualified")]
                        if "sageScore" in mapDetail.get("versions")[-1]:
                            sageScoreList += [mapDetail.get("versions")[-1].get("sageScore")]
                        else:
                            sageScoreList += [None]
                        difficultyList += [beatSaverDataPerDifficulty.get("difficulty")]
                        njsList += [beatSaverDataPerDifficulty.get("njs")]
                        offsetList += [beatSaverDataPerDifficulty.get("offset")]
                        notesList += [beatSaverDataPerDifficulty.get("notes")]
                        bombsList += [beatSaverDataPerDifficulty.get("bombs")]
                        obstaclesList += [beatSaverDataPerDifficulty.get("obstacles")]
                        npsList += [beatSaverDataPerDifficulty.get("nps")]
                        lengthList += [beatSaverDataPerDifficulty.get("length")]
                        characteristicList += [beatSaverDataPerDifficulty.get("characteristic")]
                        eventsList += [beatSaverDataPerDifficulty.get("events")]
                        chromaList += [beatSaverDataPerDifficulty.get("chroma")]
                        meList += [beatSaverDataPerDifficulty.get("me")]
                        neList += [beatSaverDataPerDifficulty.get("ne")]
                        cinemaList += [beatSaverDataPerDifficulty.get("cinema")]
                        secondsList += [beatSaverDataPerDifficulty.get("seconds")]
                        errorsList += [beatSaverDataPerDifficulty.get("paritySummary").get("errors")]
                        warnsList += [beatSaverDataPerDifficulty.get("paritySummary").get("warns")]
                        resetsList += [beatSaverDataPerDifficulty.get("paritySummary").get("resets")]
                        if (
                                scoreSaberDataPerDifficulty.get("songHash").upper() == "5536BE9C26867AB38524FA53E30FC1AB889D3251" or \
                                scoreSaberDataPerDifficulty.get(
                                    "songHash").upper() == "FFEEC65EFC5212B770D6DEED6F9AD766914D7635" or \
                                scoreSaberDataPerDifficulty.get(
                                    "songHash").upper() == "7B4445883E395FFEFC41BADCE1FA3159FADA9E3C"):
                            # 全難易度がランクなのでできること
                            urlDifficulty = 0
                            if beatSaverDataPerDifficulty.get("difficulty") == "Easy":
                                urlDifficulty = 1
                            elif beatSaverDataPerDifficulty.get("difficulty") == "Normal":
                                urlDifficulty = 3
                            elif beatSaverDataPerDifficulty.get("difficulty") == "Hard":
                                urlDifficulty = 5
                            elif beatSaverDataPerDifficulty.get("difficulty") == "Expert":
                                urlDifficulty = 7
                            elif beatSaverDataPerDifficulty.get("difficulty") == "ExpertPlus":
                                urlDifficulty = 9
                            scoreSaberStarsUrl = f"https://scoresaber.com/api/leaderboard/by-hash/{scoreSaberDataPerDifficulty.get('songHash').upper()}/info?difficulty={urlDifficulty}"
                            scoreSaberStarsResponse = requests.get(scoreSaberStarsUrl)
                            scoreSaberStarsJson = scoreSaberStarsResponse.json()
                            starsList += [scoreSaberStarsJson.get("stars")]
                        else:
                            starsList += [beatSaverDataPerDifficulty.get("stars")]
                        maxScoreList += [beatSaverDataPerDifficulty.get("maxScore")]
                        downloadUrlList += [mapDetail.get("versions")[-1].get("downloadURL")]
                        coverUrlList += [mapDetail.get("versions")[-1].get("coverURL")]
                        previewUrlList += [mapDetail.get("versions")[-1].get("previewURL")]
                        tagStr = ""
                        if "tags" in mapDetail:

                            for tag in mapDetail.get("tags"):
                                tagStr += tag + ","
                            tagStr = tagStr[:-1]
                        else:
                            tagStr = None
                        tagsList += [tagStr]

if len(idList) == 0:
    nextDf = previousDf

else:
    # DBと同じ考え方でOK
    addedDf = pd.DataFrame(columns=["id", "leaderboardId", "hash", "name", "description", "uploaderId",
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

    print(addedDf.head())

    nextDf = addedDf.append(previousDf, ignore_index=True)

# For local update, change "out" to "."
# 余分な空行が入るのでnewline設定で回避
with open(f'out/outcome.csv', 'w', encoding="utf-8", newline="\n", errors="ignore") as f:
    nextDf.to_csv(f)
