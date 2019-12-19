from sklearn.model_selection import train_test_split
import numpy as np

from RIClassificator import RIClassificator
from Data import Data
from get_data import get_data_from_csv


def test_ri_classificator():
    classes, ri, ri_doc = get_data_from_csv('test.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        ri_doc, ri, test_size=0.2, random_state=42)
    data = Data()
    data.add_classes(classes)
    data.add_data(y_train, X_train)
    ri_clss = RIClassificator(data)
    res = ri_clss.predict(X_test)
    index_t = np.array([data.name_index[t] for t in y_test])
    index_r = np.array([data.name_index[t] for t in res])
    acc = np.mean(index_t == index_r)
    print(f'ACC: {acc}')
    if acc < 0.88:
        raise AssertionError('Classificator error, acc must be > 88')
