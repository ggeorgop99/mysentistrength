import pandas as pd

df = pd.read_csv("preprocessed_datasets/reviewstars_bin.csv")
df1 = pd.read_csv("preprocessed_datasets/reviewstars_new_unproc_bin.csv")
df2 = pd.read_csv("preprocessed_datasets/reviewstars_unproc_bin.csv")
# df= df.drop(columns=['Unnamed: 2'])
# df['reviews'] = df['text_proc']
# df = df.drop(columns=['text_proc'])
# df.to_csv("preprocessed_datasets/reviewstarsbin_bin.csv", index=False)


print(df.columns)
print(df.head())
print(df1.head())
print(df2.head())