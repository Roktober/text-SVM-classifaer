"""
Preprocess csv with headers ['ri', 'ri_doc']
Train NBClassificator and save data to json
Test save load json
"""
import pandas as pd
import scipy
from RIClassificator import RIClassificator
from Data import Data
import numpy as np
from sklearn.model_selection import train_test_split
import sys
import nltk

"""
\copy (Select tax_land.utilization, utilization_bydoc From tax_land) To '~/test.csv' With CSV;
"""


def get_data_from_csv(filename: str):
    df = pd.read_csv(filename, dtype=str)
    df = df.dropna(how='all')
    unclassificated_data = df[(df['ri'].isnull()) & (df['ri_doc'].notnull())]
    classificated_data = df[(df['ri'].notnull()) & (df['ri_doc'].notnull())]
    r = RIClassificator('')
    preprocessed_classify_data = classificated_data
    preprocessed_classify_data['ri_doc'] = classificated_data['ri_doc'].apply(
        r.preprocess_text)
    preprocessed_classify_data['ri_doc'] = classificated_data['ri_doc'].apply(
        ''.join)
    preprocessed_unclassify_data = unclassificated_data['ri_doc'].apply(
        r.preprocess_text)
    preprocessed_unclassify_data = unclassificated_data['ri_doc'].apply(
        ''.join)
    classes = set(preprocessed_classify_data['ri'])
    return (classes, preprocessed_classify_data, preprocessed_unclassify_data)


def train_NB(clss, classi_data, notclassi_data):
    d = Data()
    r = RIClassificator(d)
    r.add_classes(clss)
    X_train, X_test, y_train, y_test = train_test_split(
        classi_data['ri_doc'].values.tolist(), classi_data['ri'].values.tolist(), test_size=0.2, random_state=42)
    r.add_data_without_preprocessing(X_train, y_train)
    r.build_model()
    res = r.model.predict(r.preprocessed_text_to_vec(X_test))
    r.add_data_without_preprocessing(X_test, y_test)
    index = [r.data.name_index[t] for t in y_test]
    name = r.data._save_to_json()
    acc = np.mean(res == index)
    print('acc: ', acc, f'\nData saved to {name}.json')

    return f'{name}.json', d, acc


def save_and_check_data(filename):
    clss, classi_data, notclassi_data = get_data_from_csv(filename)
    name, _d, acc = train_NB(clss, classi_data, notclassi_data)
    d = Data()
    d = d.load_from_json(name)
    print('Test data save/load')
    if (d == _d):
        print('Sucess')
    else:
        raise AssertionError('Data classes not equals after save load json')
    return d, acc


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Filename required')
        sys.exit()
    else:
        filename = sys.argv[1]
        if '.json' in filename:
            save_and_check_data(filename)
        else:
            print('Json file type required')
            sys.exit()