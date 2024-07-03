import pandas as pd

file1 = 'dirtyreviews.csv'
file2 = 'dirtyreviews1.csv' 
file3= 'dirtyreviews2.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

dfs=[df1,df2, df3]

print("First DataFrame:")
print(df1.head())
print("\nSecond DataFrame:")
print(df2.head())
print("\nThird DataFrame:")
print(df3.head())

merged_df = pd.concat(dfs, ignore_index=True)
merged_df.drop_duplicates(inplace=True)
print("\nMerged DataFrame:")
print(merged_df.head())

merged_df.to_csv('final_dirtyreviews.csv', index=False)

