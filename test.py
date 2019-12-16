from RIClassificator import RIClassificator
import json
from Data import Data
from get_data import from_csv


def test_all():
    _, acc = from_csv('test.csv')
    print('ACC: ', acc)
    if acc < 0.869:
        raise AssertionError('Acc error')
    print('test passed!')
