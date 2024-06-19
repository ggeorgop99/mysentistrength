import pandas as pd

df = pd.read_csv("preprocessed_datasets/reviewstarsbin_bin.csv")
# df= df.drop(columns=['Unnamed: 2'])
# df['reviews'] = df['text_proc']
# df = df.drop(columns=['text_proc'])
# df.to_csv("preprocessed_datasets/reviewstarsbin_bin.csv", index=False)


print(df.columns)
print(df.head())