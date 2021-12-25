## The English version of README is [here](README.md)

# RankedMapData

## これは何？
BeatSaverから取得できるランク譜面のデータのcsvです<br>
あくまで譜面そのもののデータを集めたcsvなので、ScoreSaberから取得できるPP関係のデータは含まれていません<br>
~~今は３時間ごとに更新する設定にしています~~<br>
１時間ごとに追加された譜面分だけ更新、日本時間の９時台の更新にはすべての譜面のデータを更新します。

## ダウンロード先
[こちら](https://github.com/rakkyo150/ScoreSaberRankData/releases) からダウンロードできます

## データ項目の説明
だいたいわかると思いますが、一応説明しておきます<br>
正直よくわからない項目もあるので、間違いなどありましたら教えていただけるとありがたいです<br>
|項目|説明|
|:---|:---|
|id|!bsrで使われるやつ|
|leaderboardId|ScoreSaberの各譜面のリンクの末尾にあるやつ|
|hash|譜面のハッシュ|
|name|譜面名|
|bpm|Beat Per Minute|
|duration|譜面全体の長さ(単位は秒)|
|songAuthorName|曲の作者|
|levelAuthorName|譜面の作者|
|upvotesRatio|アップボートの割合|
|uploadedAt|譜面を最初にアップロードした日時|
|automapper|自動マッピングかどうか|
|difficulty|譜面の難易度(EasyからExpertPlus)|
|createdAt|譜面の最新の更新日|
|sageScore|どれだけBeatSageで作った譜面っぽいか|
|njs|Notes Jump Speed(単位はm/s)|
|offset|オフセット|
|notes|ノーツ数|
|bombs|ボム数|
|obstacles|壁の数|
|nps|Notes Per Second|
|length|多分前後の空白地帯をのぞいた譜面の時間(単位はbeatっぽいです)|
|characteristic|譜面のプレイモード|
|events|ライトイベント数|
|chrome|クローマを使用しているかどうか|
|me|MapppingExtentionsを使用しているかどうか|
|ne|NoodleExtentionsを使用しているかどうか|
|cinema|Cinema Modに対応しているかどうか|
|seconds|多分前後の空白地帯をのぞいた譜面の時間(単位は秒)|
|errors|譜面に含まれるエラー数|
|warns|譜面に含まれるwarns数|
|resets|譜面に含まれるリセット数|


