import pandas as pd

# Read the CSV file
df = pd.read_csv("newdatasets/greek.csv")

# Keep only the "text" and "sentiment" columns
df = df[["text", "sentiment"]]

# Rename the "text" column to "reviews"
df = df.rename(columns={"text": "reviews"})

# Apply sentiment mapping based on mode
mode = "bin"  # Change to "nonbin" for non-binary mode

mode = "nonbin"

if mode == "bin":
    # Map sentiments to binary values
    sentiment_mapping = {"negative": 0, "neutral": 1, "positive": 1}
    df["sentiment"] = df["sentiment"].map(sentiment_mapping)
elif mode == "nonbin":
    # Map sentiments to non-binary values
    sentiment_mapping = {"negative": -1, "neutral": 0, "positive": 1}
    df["sentiment"] = df["sentiment"].map(sentiment_mapping)

# Save the modified DataFrame to a new CSV file
df.to_csv("newdatasets/pharm" + mode + ".csv", index=False)
