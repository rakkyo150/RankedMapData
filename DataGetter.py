import pandas as pd
import requests
from pandas import DataFrame


def get_ranked_stars_data(beat_saver_data_per_difficulty, score_saber_data_per_difficulty):
    url_difficulty = 0
    if beat_saver_data_per_difficulty.get("difficulty") == "Easy":
        url_difficulty = 1
    elif beat_saver_data_per_difficulty.get("difficulty") == "Normal":
        url_difficulty = 3
    elif beat_saver_data_per_difficulty.get("difficulty") == "Hard":
        url_difficulty = 5
    elif beat_saver_data_per_difficulty.get("difficulty") == "Expert":
        url_difficulty = 7
    elif beat_saver_data_per_difficulty.get("difficulty") == "ExpertPlus":
        url_difficulty = 9
    score_saber_ranked_stars_data_url = f"https://scoresaber.com/api/leaderboard/by-hash/" \
                                        f"{score_saber_data_per_difficulty.get('songHash').upper()}" \
                                        f"/info?difficulty={url_difficulty}" \
                                        f"&gameMode={'Solo' + beat_saver_data_per_difficulty.get('characteristic')}"
    score_saber_ranked_stars_data_response = requests.get(score_saber_ranked_stars_data_url)
    score_saber_ranked_stars_data_json = score_saber_ranked_stars_data_response.json()
    return score_saber_ranked_stars_data_json


class DataGetter:
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

    def get_data(self) -> DataFrame:
        previous_hash_list = []
        get_data_from_beat_saver_count = 0
        page_number = 0
        while True:
            page_number += 1
            # ランク譜面の情報を最新のものから順に
            score_saber_response = requests.get(
                f"https://scoresaber.com/api/leaderboards?ranked=true&category=1&sort=0&page={page_number}")
            score_saber_json_data = score_saber_response.json()

            if len(score_saber_json_data.get("leaderboards")) == 0:
                break

            for score_saber_data_per_difficulty in score_saber_json_data.get("leaderboards"):
                # 小文字だけのハッシュや大文字小文字両方のハッシュが存在する譜面の対応のため、比較するときは大文字にそろえる
                # 一度ハッシュを取得すれば他難易度の同ハッシュは重複するのでいらない
                if score_saber_data_per_difficulty.get("songHash").upper() in previous_hash_list:
                    continue

                get_data_from_beat_saver_count += 1
                print(f"{get_data_from_beat_saver_count}回目の取得")
                print(score_saber_data_per_difficulty.get("songName"))
                previous_hash_list.append(score_saber_data_per_difficulty.get("songHash").upper())
                # ハッシュが一致する譜面の全難易度の情報を取得していく
                beat_saver_response = requests.get(
                    f'https://api.beatsaver.com/maps/hash/{score_saber_data_per_difficulty.get("songHash")}')

                # ScoreSaberに情報はあるけどBeatSaverでは消されたっぽい譜面
                if beat_saver_response.status_code == 404:
                    print(f"{beat_saver_response.status_code} Not Found: "
                          f"{score_saber_data_per_difficulty.get('songName')}-"
                          f"{score_saber_data_per_difficulty.get('id')}-"
                          f"{score_saber_data_per_difficulty.get('songHash')}")
                    continue

                map_detail = beat_saver_response.json()
                map_difficulty = map_detail.get("versions")[-1].get("diffs")

                for beatSaverDataPerDifficulty in map_difficulty:

                    score_saber_ranked_stars_json = get_ranked_stars_data(
                        beatSaverDataPerDifficulty, score_saber_data_per_difficulty)

                    # 重いけどBeatSaverのランクかどうかの情報は信頼性に欠ける
                    if not score_saber_ranked_stars_json.get("ranked"):
                        continue

                    self.add_data(beatSaverDataPerDifficulty, map_detail,
                                  score_saber_data_per_difficulty, score_saber_ranked_stars_json)

        # DBと同じ考え方でOK
        outcome_df = self.set_data()
        print(outcome_df.head())

        return outcome_df

    def add_data(self, beatSaverDataPerDifficulty, map_detail, score_saber_data_per_difficulty,
                 score_saber_stars_json):
        self.idList += [map_detail.get("id")]
        self.leaderboardIdList += [
            score_saber_data_per_difficulty.get("id")]
        self.hashList += [score_saber_data_per_difficulty.get("songHash")]
        self.nameList += [map_detail.get("name")]
        self.descriptionList += [map_detail.get("description")]
        self.uploaderIdList += [map_detail.get("uploader").get("id")]
        self.uploaderNameList += [map_detail.get("uploader").get("name")]
        self.uploaderHashList += [map_detail.get("uploader").get("hash")]
        self.uploaderAvatarList += [
            map_detail.get("uploader").get("avatar")]
        self.uploaderLoginTypeList += [
            map_detail.get("uploader").get("type")]
        self.uploaderCuratorList += [
            map_detail.get("uploader").get("curator")]
        self.bpmList += [map_detail.get("metadata").get("bpm")]
        self.durationList += [map_detail.get("metadata").get("duration")]
        self.songAuthorNameList += [
            map_detail.get("metadata").get("songAuthorName")]
        self.levelAuthorNameList += [
            map_detail.get("metadata").get("levelAuthorName")]
        self.upvotesList += [map_detail.get("stats").get("upvotes")]
        self.downvotesList += [map_detail.get("stats").get("downvotes")]
        self.upvotesRatioList += [map_detail.get("stats").get("score")]
        self.uploadedAtList += [map_detail.get("uploaded")]
        self.createdAtList += [map_detail.get("createdAt")]
        self.updatedAtList += [map_detail.get("updatedAt")]
        self.lastPublishedAtList += [map_detail.get("lastPublishedAt")]
        self.automapperList += [map_detail.get("automapper")]
        self.qualifiedList += [map_detail.get("qualified")]
        if "sageScore" in map_detail.get("versions")[-1]:
            self.sageScoreList += [
                map_detail.get("versions")[-1].get("sageScore")]
        else:
            self.sageScoreList += [None]
        self.difficultyList += [beatSaverDataPerDifficulty.get("difficulty")]
        self.njsList += [beatSaverDataPerDifficulty.get("njs")]
        self.offsetList += [beatSaverDataPerDifficulty.get("offset")]
        self.notesList += [beatSaverDataPerDifficulty.get("notes")]
        self.bombsList += [beatSaverDataPerDifficulty.get("bombs")]
        self.obstaclesList += [beatSaverDataPerDifficulty.get("obstacles")]
        self.npsList += [beatSaverDataPerDifficulty.get("nps")]
        self.lengthList += [beatSaverDataPerDifficulty.get("length")]
        self.characteristicList += [beatSaverDataPerDifficulty.get("characteristic")]
        self.eventsList += [beatSaverDataPerDifficulty.get("events")]
        self.chromaList += [beatSaverDataPerDifficulty.get("chroma")]
        self.meList += [beatSaverDataPerDifficulty.get("me")]
        self.neList += [beatSaverDataPerDifficulty.get("ne")]
        self.cinemaList += [beatSaverDataPerDifficulty.get("cinema")]
        self.secondsList += [beatSaverDataPerDifficulty.get("seconds")]
        self.errorsList += [
            beatSaverDataPerDifficulty.get("paritySummary").get("errors")]
        self.warnsList += [beatSaverDataPerDifficulty.get("paritySummary").get("warns")]
        self.resetsList += [
            beatSaverDataPerDifficulty.get("paritySummary").get("resets")]
        self.starsList += [score_saber_stars_json.get("stars")]
        self.maxScoreList += [beatSaverDataPerDifficulty.get("maxScore")]
        self.downloadUrlList += [
            map_detail.get("versions")[-1].get("downloadURL")]
        self.coverUrlList += [
            map_detail.get("versions")[-1].get("coverURL")]
        self.previewUrlList += [
            map_detail.get("versions")[-1].get("previewURL")]
        tag_str = ""
        if "tags" in map_detail:
            for tag in map_detail.get("tags"):
                tag_str += tag + ","
            tag_str = tag_str[:-1]
        else:
            tag_str = None
        self.tagsList += [tag_str]

    def set_data(self):
        return pd.DataFrame(
            columns=["id", "leaderboardId", "hash", "name", "description", "uploaderId",
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
            data={"id": self.idList, "leaderboardId": self.leaderboardIdList,
                  "hash": self.hashList,
                  "name": self.nameList,
                  "description": self.descriptionList, "uploaderId": self.uploaderIdList,
                  "uploaderName": self.uploaderNameList,
                  "uploaderHash": self.uploaderHashList,
                  "uploaderAvatar": self.uploaderAvatarList,
                  "uploaderLoginType": self.uploaderLoginTypeList,
                  "uploaderCurator": self.uploaderCuratorList,
                  "bpm": self.bpmList, "duration": self.durationList,
                  "songAuthorName": self.songAuthorNameList,
                  "levelAuthorName": self.levelAuthorNameList, "upvotes": self.upvotesList,
                  "downvotes": self.downvotesList,
                  "upvotesRatio": self.upvotesRatioList, "uploadedAt": self.uploadedAtList,
                  "createdAt": self.createdAtList,
                  "updatedAt": self.updatedAtList, "lastPublishedAt": self.lastPublishedAtList,
                  "automapper": self.automapperList,
                  "qualified": self.qualifiedList, "difficulty": self.difficultyList,
                  "sageScore": self.sageScoreList, "njs": self.njsList,
                  "offset": self.offsetList,
                  "notes": self.notesList, "bombs": self.bombsList,
                  "obstacles": self.obstaclesList,
                  "nps": self.npsList,
                  "length": self.lengthList, "characteristic": self.characteristicList,
                  "events": self.eventsList,
                  "chroma": self.chromaList, "me": self.meList, "ne": self.neList,
                  "cinema": self.cinemaList,
                  "seconds": self.secondsList,
                  "errors": self.errorsList, "warns": self.warnsList, "resets": self.resetsList,
                  "stars": self.starsList,
                  "maxScore": self.maxScoreList, "downloadUrl": self.downvotesList,
                  "coverUrl": self.coverUrlList,
                  "previewUrl": self.previewUrlList, "tags": self.tagsList})
