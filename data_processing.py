import csv
import numpy as np
import pandas as pd
import seaborn as sns

def process_data():
    with open('test1.csv','r', encoding='utf-8') as dest_f:
        data_iter = csv.reader(dest_f,
                               delimiter = ",")
        data = [data for data in data_iter]
    data_array = np.asarray(data)
    rev = data_array[1]
    for i in range(len(data_array[1])):
        data_array[1][i] = data_array[1][i].replace('"','')
        data_array[1][i] = data_array[1][i].replace('...\nFull Review','')
        data_array[1][i] = data_array[1][i].replace('\n','')
        data_array[1][i] = data_array[1][i].replace('/','')
        data_array[1][i] = data_array[1][i].replace('\n','')
        data_array[1][i] = data_array[1][i].replace('br...','')

    for i in range(len(data_array[3])):
        data_array[3][i] = data_array[3][i].replace('Rated','')
        data_array[3][i] = data_array[3][i].replace('stars out of five stars','')
        data_array[3][i] = data_array[3][i].replace(' ','')

    data_array.reshape(5,-1)
    print(type(data_array),data_array.shape)

    ds = []
    columns = ['Name','Review','UpVotes','Rating','Date']
    ds.append(columns)


    for j in range(len(data_array[0])):
        temp = []
        for i in range(data_array.shape[0]):
            try:
                temp.append(data_array[i][j])
            except:
                continue
    ds.append(temp)

    print(ds)
    print(len(ds),len(ds[0]))

    with open("processed1.csv", "w", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(ds)

