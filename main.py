import DataGetter

print("全更新")
dataGetter = DataGetter.DataGetter()

outcome_df = dataGetter.get_data(False)

dataGetter.save(outcome_df, f'out/outcome.csv')