import requests
from beatsaver.beatsaver import BeatSaver
import pandas as pd
import matplotlib.pyplot as plt
import time

beatSaver=BeatSaver()
beatSaberAccessCount=0
previousHash= ""

mapList=[]
difficultyList=[]
njsList=[]
offsetList=[]
lengthList=[]
npsList=[]
notesList=[]
obstaclesList=[]
bombsList=[]
starsList=[]

df=pd.DataFrame(columns=["song","difficulty","njs","offset","length","nps","notes","obstacles","bombs","stars"])

# 191ページ目まである
for i in range(1,192):
    response=requests.get(f"https://scoresaber.com/api/leaderboards?ranked=true&category=1&sort=0&page={i}")
    print(response.text)
    jsonData=response.json()
    for j in jsonData["leaderboards"]:
        print(j["songName"])
        # print(j["songHash"])
        if j["songHash"]==previousHash:
            pass
        else:
            previousHash=j["songHash"]
            if beatSaberAccessCount%100==0:
                time.sleep(30)
            elif beatSaberAccessCount==976:
                time.sleep(60)
            beatSaberAccessCount += 1
            print(f"{beatSaberAccessCount}回目の取得")
            mapDetail=beatSaver.get_maps_hash(j["songHash"])
            mapDifficulty=mapDetail.versions[-1].diffs

            for k in mapDifficulty:

                if k.stars is not None:

                    mapName=j["songName"]+"-"+k.difficulty+"-"+j["songHash"]

                    mapList+=[mapName]
                    njsList+=[k.njs]
                    offsetList+=[k.offset]
                    lengthList+=[k.length]
                    npsList+=[k.nps]
                    notesList+=[k.notes]
                    obstaclesList+=[k.obstacles]
                    bombsList+=[k.bombs]
                    starsList+=[k.stars]

# DBと同じ考え方でOK
df=pd.DataFrame(columns=["njs","offset","length","nps","notes","obstacles","bombs","stars"],
                index=mapList,
                data={"njs":njsList,"offset":offsetList,
                      "length":lengthList,"nps":npsList,"notes":notesList,"obstacles":obstaclesList,
                      "bombs":bombsList,"stars":starsList})

print(df.head())

df.plot.box()
plt.savefig("box.png")
plt.show()

plt.figure()

standardDf=(df-df.mean())/df.std()
standardDf.plot.box()
plt.savefig("standardBox.png")
plt.show()
plt.close()

df.to_csv("outcome.csv")