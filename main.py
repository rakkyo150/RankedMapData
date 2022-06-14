import pandas as pd

import DataGetter

print("全更新")
dataGetter = DataGetter.DataGetter()

outcomeDf = dataGetter.get_data()

# For local update, change "out" to "."
# 余分な空行が入るのでnewline設定で回避
with open(f'out/outcome.csv', 'w', encoding="utf-8", newline="\n", errors="ignore") as f:
    outcomeDf.to_csv(f)
