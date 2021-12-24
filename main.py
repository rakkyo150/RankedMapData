import requests
from beatsaver.beatsaver import BeatSaver
import pandas as pd
import matplotlib.pyplot as plt
import time

beatSaberAccessCount=0
previousHash= ""

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

df=pd.DataFrame(columns=["song","difficulty","njs","offset","length","nps","notes","obstacles","bombs","stars"])

# 191ページ目まである
pageNumber=0
while True:
    pageNumber += 1
    scoreSaberResponse=requests.get(f"https://scoresaber.com/api/leaderboards?ranked=true&category=1&sort=0&page={pageNumber}")
    print(scoreSaberResponse.text)
    jsonData=scoreSaberResponse.json()
    if len(jsonData["leaderboards"])==0:
        break
    for j in jsonData["leaderboards"]:
        print(j["songName"])
        # print(j["songHash"])
        if j["songHash"]==previousHash:
            pass
        else:
            previousHash=j["songHash"]
            time.sleep(1)
            beatSaberAccessCount += 1
            print(f"{beatSaberAccessCount}回目の取得")
            beatSaverResponse=requests.get(f'https://api.beatsaver.com/maps/hash/{j["songHash"]}')

            # 消された譜面も含まれているっぽいので
            if beatSaverResponse.status_code==404:
                print(beatSaverResponse.status_code)
                pass

            else:
                mapDetail=beatSaverResponse.json()
                print(beatSaverResponse.text)
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

df.plot.box()
plt.savefig("box.png")
plt.show()

"""
plt.figure()
standardDf=(df-df.mean())/df.std()
standardDf.plot.box()
plt.savefig("standardBox.png")
plt.show()
"""

plt.close()

df.to_csv("outcome.csv")