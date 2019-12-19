from RIClassificator import RIClassificator
import json
from Data import Data
from get_data import from_csv

import nltk


def test_all():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger_ru')
    _, acc = from_csv('test.csv')
    print('ACC: ', acc)
    if acc < 0.869:
        raise AssertionError('Acc error')
    print('test passed!')
