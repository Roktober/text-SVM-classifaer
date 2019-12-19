from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from Data import Data
import numpy as np
import time
from ClassificatorDAO import ClassificatorDAO

import logging


class RIClassificator(object):

    def __init__(self, data: Data,
                 classificatorDAO: ClassificatorDAO = None, source=None):
        self.count_vect = CountVectorizer()
        self.data = data
        self.model = None
        self.source = source if source else 1
        self.classificatorDAO = classificatorDAO

        if classificatorDAO:
            self.get_data()
            self.build_model()

    def preprocessed_text_to_vec(self, text: list, source=1):
        self.check_source(source)
        return self.count_vect.transform(text)

    def build_model(self):
        t = time.time()
        X_train, Y_train = self.data.document_data, self.data.class_index_document_data
        X_train = self.count_vect.fit_transform(X_train)
        self.model = SVC(
            C=1,
            kernel='linear',
            gamma='auto',
            random_state=42,
            decision_function_shape='ovr'
        ).fit(
            X_train,
            Y_train)
        logging.info(
            f'{time.time() - t} s Build model time with data shape: {len(Y_train)}')

    def predict(self, text: list, source=1):
        self.check_source(source)
        t = time.time()
        if self.model is None:
            self.build_model()
        vectorized_text = self.preprocessed_text_to_vec(
            text)

        predict = self.model.predict(vectorized_text)
        result = [self.data.index_name[index] for index in predict]
        logging.info(
            f'Predict {len(text)} values with {len(self.data.class_index_document_data)} datasets, predict time {time.time()-t}')
        return result

    def check_source(self, source=1):
        if source != self.source:
            self.source = source
            self.get_data()

    def data_spliter(self, data):
        clss, clss_id = [], []
        for el in data:
            clss.append(el[0])
            clss_id.append(el[1])
        return clss_id, clss

    def add_data(self, val, clss, source=1):
        # TODO: protect bean from similar data
        self.check_source(source)
        self.data.add_data(clss, val)
        self.classificatorDAO.insert_data_for_train(val, clss, source)
        self.build_model()

    def get_data(self):
        data = self.classificatorDAO.select_data_for_train(self.source)
        self.data = Data()
        self.data.add_data(*self.data_spliter(data))
