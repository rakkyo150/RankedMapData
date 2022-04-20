import os
import requests
import pandas as pd
import time
import io
import datetime

beatSaberAccessCount=0
previousHashList= []

idList=[]
leaderboardIdList=[]
hashList=[]
nameList=[]
bpmList=[]
# 曲全体の長さ
durationList=[]
songAuthorNameList=[]
levelAuthorNameList=[]
upvotesRatioList=[]
# 初回アップロード
uploadedAtList=[]
automapperList=[]
# 最終アップロード
createdAtList=[]
sageScoreList=[]
difficultyList=[]
njsList=[]
offsetList=[]
notesList=[]
bombsList=[]
obstaclesList=[]
npsList=[]
# beat換算っぽい
lengthList=[]
characteristicList=[]
eventsList=[]
chromaList=[]
meList=[]
neList=[]
cinemaList=[]
secondsList=[]
errorsList=[]
warnsList=[]
resetsList=[]
starsList=[]

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
previousDf = pd.DataFrame(columns=["id","leaderboardId","hash","name","bpm","duration","songAuthorName","levelAuthorName",
                         "upvotesRatio","uploadedAt","automapper","difficulty","createdAt","sageScore",
                         "njs","offset","notes","bombs","obstacles","nps","length","characteristic",
                         "events","chroma","me","ne","cinema","seconds","errors","warns","resets","stars"],
                          index=[])
previousHashList = []

pageNumber=0
while True:
    pageNumber += 1
    # ランク譜面の情報を最新のものから順に
    scoreSaberResponse=requests.get(f"https://scoresaber.com/api/leaderboards?ranked=true&category=1&sort=0&page={pageNumber}")
    jsonData=scoreSaberResponse.json()
    if len(jsonData["leaderboards"])==0:
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
            beatSaverResponse=requests.get(f'https://api.beatsaver.com/maps/hash/{j["songHash"]}')

            # ScoreSaberに情報はあるけどBeatSaverでは消されたっぽい譜面
            if beatSaverResponse.status_code==404:
                print(f"{beatSaverResponse.status_code} Not Found: {j['songName']}-{j['id']}-{j['songHash']}")
                pass

            else:
                mapDetail=beatSaverResponse.json()
                mapDifficulty=mapDetail["versions"][-1]["diffs"]

                for k in mapDifficulty:

                    if "stars" in k:
                        idList+=[mapDetail["id"]]
                        leaderboardIdList+=[j["id"]]
                        hashList += [j["songHash"]]
                        nameList+=[mapDetail["name"]]
                        bpmList+=[mapDetail["metadata"]["bpm"]]
                        durationList+=[mapDetail["metadata"]["duration"]]
                        songAuthorNameList+=[mapDetail["metadata"]["songAuthorName"]]
                        levelAuthorNameList+=[mapDetail["metadata"]["levelAuthorName"]]
                        upvotesRatioList+=[mapDetail["stats"]["score"]]
                        uploadedAtList+=[mapDetail["uploaded"]]
                        automapperList+=[mapDetail["automapper"]]
                        createdAtList+=[mapDetail["versions"][-1]["createdAt"]]
                        if "sageScore" in mapDetail["versions"][-1]:
                            sageScoreList+=[mapDetail["versions"][-1]["sageScore"]]
                        else:
                            sageScoreList+=[None]
                        difficultyList+=[k["difficulty"]]
                        njsList+=[k["njs"]]
                        offsetList+=[k["offset"]]
                        notesList += [k["notes"]]
                        bombsList += [k["bombs"]]
                        obstaclesList += [k["obstacles"]]
                        npsList+=[k["nps"]]
                        lengthList += [k["length"]]
                        characteristicList+=[k["characteristic"]]
                        eventsList+=[k["events"]]
                        chromaList+=[k["chroma"]]
                        meList+=[k["me"]]
                        neList+=[k["ne"]]
                        cinemaList+=[k["cinema"]]
                        secondsList+=[k["seconds"]]
                        errorsList+=[k["paritySummary"]["errors"]]
                        warnsList+=[k["paritySummary"]["warns"]]
                        resetsList+=[k["paritySummary"]["resets"]]
                        starsList+=[k["stars"]]


if len(idList)==0:
    nextDf=previousDf

else:
    # DBと同じ考え方でOK
    df=pd.DataFrame(columns=["id","leaderboardId","hash","name","bpm","duration","songAuthorName","levelAuthorName",
                             "upvotesRatio","uploadedAt","automapper","difficulty","createdAt","sageScore",
                             "njs","offset","notes","bombs","obstacles","nps","length","characteristic",
                             "events","chroma","me","ne","cinema","seconds","errors","warns","resets","stars"],
                    data={"id":idList,"leaderboardId":leaderboardIdList,"hash":hashList,"name":nameList,
                          "bpm":bpmList,"duration":durationList,"songAuthorName":songAuthorNameList,
                          "levelAuthorName":levelAuthorNameList,"upvotesRatio":upvotesRatioList,
                          "uploadedAt":uploadedAtList,"automapper":automapperList,"difficulty":difficultyList,
                          "createdAt":createdAtList,"sageScore":sageScoreList,"njs":njsList,"offset":offsetList,
                          "notes":notesList,"bombs":bombsList,"obstacles":obstaclesList,"nps":npsList,
                          "length":lengthList,"characteristic":characteristicList,"events":eventsList,
                          "chroma":chromaList,"me":meList,"ne":neList,"cinema":cinemaList,"seconds":secondsList,
                          "errors":errorsList,"warns":warnsList,"resets":resetsList,"stars":starsList})

    print(df.head())

    nextDf=df.append(previousDf,ignore_index=True)


# For local update, change "out" to "."
# 余分な空行が入るのでnewline設定で回避
with open(f'out/outcome.csv','w',encoding="utf-8",newline="\n",errors="ignore") as f:
    nextDf.to_csv(f)