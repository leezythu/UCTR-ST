from os import sep
import pandas as pd
import json

from sqlalchemy import false
with open("pseudo_labels.json") as f:
    pseudo_labels = json.load(f)
    pseudo_labels = pseudo_labels["preds"]

TSV_FOLDER = '/home/lzy/data/UCTR/sem-tab-fact/tsv/'
train_file = "train_3way_set.tsv"

dev_data = pd.read_csv(TSV_FOLDER+train_file, sep='\t')
assert len(dev_data) == len(pseudo_labels)
for i in range(len(dev_data)):
    dev_data.loc[i,'answer_text'] = pseudo_labels[i]

dev_data.to_csv("pseudo_train.tsv",sep='\t',index = False)
