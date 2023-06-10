import unittest
import DataGetter
import pandas as pd
import csv

class TestGetDataPerPage(unittest.TestCase):
    dataGetter = DataGetter.DataGetter()
    outcome_df = None

    def test_get_data_per_page_success(self):
        # Set up initial values for test
        previous_hash_list = []
        get_data_from_beat_saver_count = 0
        page_number = 1
        result = False
        if len(self.dataGetter.set_data().index) == 0:
            get_data_from_beat_saver_count, result = self.dataGetter.get_data_per_page(previous_hash_list, get_data_from_beat_saver_count, page_number)

        # Make assertions about the results
        self.assertTrue(result)
        self.assertNotEqual(len(self.dataGetter.idList), 0)
        # self.assertEqual(self.dataGetter.songSubNameList[0], '')

    def test_get_data_per_page_failure(self):

        # Set up initial values for test
        previous_hash_list = []
        get_data_from_beat_saver_count = 0
        page_number = 999999
        dataGetterFailure = DataGetter.DataGetter()

        # Call the function to be tested
        get_data_from_beat_saver_count, result = dataGetterFailure.get_data_per_page(previous_hash_list, get_data_from_beat_saver_count, page_number)

        # Make assertions about the results
        self.assertFalse(result)
        self.assertEqual(get_data_from_beat_saver_count, 0)
        self.assertEqual(len(dataGetterFailure.idList), 0)
        
    def test_set_data(self):
        # Set up initial values for test
        if len(self.dataGetter.set_data().index) == 0:
            previous_hash_list = []
            get_data_from_beat_saver_count = 0
            page_number = 1
            _ = self.dataGetter.get_data_per_page(previous_hash_list, get_data_from_beat_saver_count, page_number)

        # Call the function to be tested
        self.outcome_df = self.dataGetter.set_data()

        # Make assertions about the results
        self.assertIsNotNone(self.outcome_df.iloc[1, 0])
        # self.assertEqual(outcome_df.at[outcome_df.index[0], 'songSubName'], "")

    def test_save(self):
        if len(self.dataGetter.set_data().index) == 0:
            previous_hash_list = []
            get_data_from_beat_saver_count = 0
            page_number = 1
            _ = self.dataGetter.get_data_per_page(previous_hash_list,
                                                  get_data_from_beat_saver_count, page_number)
        if self.outcome_df is None:
            self.outcome_df = self.dataGetter.set_data()

        self.dataGetter.save(self.outcome_df, f'outcome_test.csv')

        # outcome_test.csvを読み込む
        df = pd.read_csv(f'outcome_test.csv', sep=",", index_col=0, encoding="utf-8", na_filter=False)
        # dfとoutcome_dfが同じかどうかを確認する
        self.assertTrue(self.outcome_df["id"].equals(df["id"]))
        self.assertTrue(self.outcome_df["leaderboardId"].equals(df["leaderboardId"]))
        self.assertTrue(self.outcome_df["hash"].equals(df["hash"]))
        self.assertTrue(self.outcome_df["name"].equals(df["name"]))
        self.assertTrue(self.outcome_df["description"].equals(df["description"]))
        self.assertTrue(self.outcome_df["uploaderId"].equals(df["uploaderId"]))
        self.assertTrue(self.outcome_df["uploaderName"].equals(df["uploaderName"]))
        self.assertTrue(self.outcome_df["uploaderHash"].equals(df["uploaderHash"]))
        self.assertTrue(self.outcome_df["uploaderAvatar"].equals(df["uploaderAvatar"]))
        self.assertTrue(self.outcome_df["uploaderLoginType"].equals(df["uploaderLoginType"]))
        self.assertTrue(self.outcome_df["uploaderCurator"].equals(df["uploaderCurator"]))
        self.assertTrue(self.outcome_df["uploaderVerifiedMapper"].equals(df["uploaderVerifiedMapper"]))
        self.assertTrue(self.outcome_df["bpm"].equals(df["bpm"]))
        self.assertTrue(self.outcome_df["duration"].equals(df["duration"]))
        self.assertTrue(self.outcome_df["songName"].equals(df["songName"]))
        self.assertTrue(self.outcome_df["songSubName"].equals(df["songSubName"]))
        self.assertTrue(self.outcome_df["songAuthorName"].equals(df["songAuthorName"]))
        self.assertTrue(self.outcome_df["levelAuthorName"].equals(df["levelAuthorName"]))
        self.assertTrue(self.outcome_df["plays"].equals(df["plays"]))
        self.assertTrue(self.outcome_df["dailyPlays"].equals(df["dailyPlays"]))
        self.assertTrue(self.outcome_df["downloads"].equals(df["downloads"]))
        self.assertTrue(self.outcome_df["upvotes"].equals(df["upvotes"]))
        self.assertTrue(self.outcome_df["downvotes"].equals(df["downvotes"]))
        self.assertTrue(self.outcome_df["upvotesRatio"].equals(df["upvotesRatio"]))
        self.assertTrue(self.outcome_df["uploadedAt"].equals(df["uploadedAt"]))
        self.assertTrue(self.outcome_df["createdAt"].equals(df["createdAt"]))
        self.assertTrue(self.outcome_df["updatedAt"].equals(df["updatedAt"]))
        self.assertTrue(self.outcome_df["lastPublishedAt"].equals(df["lastPublishedAt"]))
        self.assertTrue(self.outcome_df["automapper"].equals(df["automapper"]))
        self.assertTrue(self.outcome_df["qualified"].equals(df["qualified"]))
        self.assertTrue(self.outcome_df["loved"].equals(df["loved"]))
        self.assertTrue(self.outcome_df["difficulty"].equals(df["difficulty"]))
        self.assertTrue(self.outcome_df["sageScore"].equals(df["sageScore"]))
        self.assertTrue(self.outcome_df["njs"].equals(df["njs"]))
        self.assertTrue(self.outcome_df["offset"].equals(df["offset"]))
        self.assertTrue(self.outcome_df["notes"].equals(df["notes"]))
        self.assertTrue(self.outcome_df["bombs"].equals(df["bombs"]))
        self.assertTrue(self.outcome_df["obstacles"].equals(df["obstacles"]))
        self.assertTrue(self.outcome_df["nps"].equals(df["nps"]))
        self.assertTrue(self.outcome_df["length"].equals(df["length"]))
        self.assertTrue(self.outcome_df["characteristic"].equals(df["characteristic"]))
        self.assertTrue(self.outcome_df["events"].equals(df["events"]))
        self.assertTrue(self.outcome_df["chroma"].equals(df["chroma"]))
        self.assertTrue(self.outcome_df["me"].equals(df["me"]))
        self.assertTrue(self.outcome_df["ne"].equals(df["ne"]))
        self.assertTrue(self.outcome_df["cinema"].equals(df["cinema"]))
        self.assertTrue(self.outcome_df["seconds"].equals(df["seconds"]))
        self.assertTrue(self.outcome_df["errors"].equals(df["errors"]))
        self.assertTrue(self.outcome_df["warns"].equals(df["warns"]))
        self.assertTrue(self.outcome_df["resets"].equals(df["resets"]))
        self.assertTrue(self.outcome_df["positiveModifiers"].equals(df["positiveModifiers"]))
        self.assertTrue(self.outcome_df["stars"].equals(df["stars"]))
        self.assertTrue(self.outcome_df["maxScore"].equals(df["maxScore"]))
        self.assertTrue(self.outcome_df["downloadUrl"].equals(df["downloadUrl"]))
        self.assertTrue(self.outcome_df["coverUrl"].equals(df["coverUrl"]))
        self.assertTrue(self.outcome_df["previewUrl"].equals(df["previewUrl"]))
        self.assertTrue(self.outcome_df["tags"].equals(df["tags"]))

if __name__ == '__main__':
    unittest.main()