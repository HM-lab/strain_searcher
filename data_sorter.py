import os
import glob
import pandas as pd
import numpy as np

def data_read():
    data_list = glob.glob('datasheets/*.xl*')
    return data_list

def keyword_load(input_keyword):
    data_index = pd.read_csv('datasheets/name_dict.csv', index_col=0)
    data_index = data_index.fillna('').astype(str).apply(lambda x: x.str.upper())

    y_list = data_index.iloc[:,0].values.tolist()
    orf_list = data_index.iloc[:,1].values.tolist()

    input_keyword = str(input_keyword).upper()
    input_keywords = input_keyword.split(',')

    keywords = []
    for keyword in input_keywords:
        if keyword in y_list:
            keywords.append(keyword)
            keywords.append(orf_list[y_list.index(keyword)])
        elif keyword in orf_list:
            keywords.append(keyword)
            keywords.append(y_list[orf_list.index(keyword)])

    return keywords

def data_search(data_list, input_keyword):
    keywords = keyword_load(input_keyword)

    output_data_list = {}

    for data in data_list:
        data_name = os.path.basename(data)
        output_data = pd.DataFrame()
        df = pd.read_excel(data)
        df = df.fillna('').astype(str).apply(lambda x: x.str.upper())

        for keyword in keywords:
            df_nan = df.where(df == keyword)
            df_searched = df[df_nan.isnull().all(axis=1) == False]
            output_data = pd.concat([output_data, df_searched], axis=0, sort=False)
            output_data = output_data.drop_duplicates()

        if len(output_data) != 0:
            output_data_list.update([(data_name, output_data)])
    
    return output_data_list

