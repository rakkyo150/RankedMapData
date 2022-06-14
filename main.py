import pandas as pd

import DataGetter

print("全更新")
dataGetter = DataGetter.DataGetter()

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

nextDf = dataGetter.get_data(previousDf)

# For local update, change "out" to "."
# 余分な空行が入るのでnewline設定で回避
with open(f'out/outcome.csv', 'w', encoding="utf-8", newline="\n", errors="ignore") as f:
    nextDf.to_csv(f)
