import pandas as pd
import csv
from itertools import zip_longest
from difflib import SequenceMatcher
import os
import argparse
from utils import generate_unique_filename

# Define the command-line arguments
parser = argparse.ArgumentParser(description='Train a sentiment analysis model.')
parser.add_argument('--mode', type=str, required=True, choices=['bin', 'nonbin'], help='Mode of the model: nonbin or bin')
parser.add_argument('--file_name', type=str, required=True, help='Name of file to preprocess')
args = parser.parse_args()

# Access the mode arguments
mode = args.mode
file_name = args.file_name

data = pd.read_csv("../mysentistrength/dataset/dirtyreviews.csv",encoding = "utf-8")
data=data.drop('topic', axis=1)
data=data.drop('title', axis=1)

data=data.dropna()
data=data.drop_duplicates(subset=['comment'], keep='first')
temp=[]
temp=data['stars'].values.tolist()
name=f'{file_name}_{mode}'
if mode=='bin':
	for i in range(0,len(data['stars'])):
		
		if int(temp[i])<=3:
			temp[i]=0;
		else:
			temp[i]=1;	

else:
	for i in range(0,len(data['stars'])):
		
		if int(temp[i])<=2:
			temp[i]=-1;
		elif int(temp[i])==3:
			temp[i]=0;
		else:		
			temp[i]=1;
data['stars']=temp

cols=data.columns.tolist()
cols = cols[-1:] + cols[:-1]
data=data[cols]
file_path = os.path.join('../neuralnet/datasets', file_name)
data.to_csv(name+'short.csv',header=['reviews','sentiment'],index=False,encoding = "utf-8")
