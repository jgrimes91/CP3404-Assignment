import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
import matplotlib.pyplot as plt

data = pd.read_csv('smoking_driking_dataset_Ver01.csv',header='infer')
data_copy = data.copy()
data = data.replace('N',0)
data = data.replace('Y',1)
data = data.replace('Male',0)
data = data.replace('Female',1)

data = data[['sex','age','DRK_YN']]
data['age'] = pd.qcut(data['age'],5,labels=[0,1,2,3,4])
data = data.fillna(0)

data['age'] = data['age'].replace(0,'<=35')
data['age'] = data['age'].replace(1,'<=45')
data['age'] = data['age'].replace(2,'<=50')
data['age'] = data['age'].replace(3,'<=60')
data['age'] = data['age'].replace(4,'<=70')

items = set()
for col in data:
    items.update(data[col].unique())
print(items)

itemset = set(items)
encoded_vals = []
for index, row in data.iterrows():
    rowset = set(row)
    labels = {}
    uncommons = list(itemset - rowset)
    commons = list(itemset.intersection(rowset))
    for uc in uncommons:
        labels[uc] = 0
    for com in commons:
        labels[com] = 1
    encoded_vals.append(labels)
encoded_vals[0]
ohe_df = pd.DataFrame(encoded_vals)
# print(ohe_df)

freq_items = apriori(ohe_df, min_support = 0.2, use_colnames = True, verbose = 1)
print(freq_items)

rules = association_rules(freq_items, metric="confidence", min_threshold=0.5)
print(rules)

data_test_file = open('data_test.csv','w')
for line in data['age']:
    data_test_file.write(line)
    data_test_file.write("\n")

data_test_file.close()
print(data)