import pandas as pd

file1 = 'dirtyreviews.csv'
file2 = 'dirtyreviews1.csv' 

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

print("First DataFrame:")
print(df1.head())
print("\nSecond DataFrame:")
print(df2.head())

merged_df = pd.concat([df1, df2])
merged_df.drop_duplicates(inplace=True)
print("\nMerged DataFrame:")
print(merged_df.head())

merged_df.to_csv('dirty_reviews.csv', index=False)

