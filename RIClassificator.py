import scipy
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn import metrics

from Porter import Porter
from Data import Data

import time


class RIClassificator(object):

    def __init__(self, data: Data):
        # nltk.download('punkt')
        # nltk.download('averaged_perceptron_tagger_ru')
        self.stemmer = Porter
        self.count_vect = CountVectorizer()
        self.data = data
        self.model = None

    def preprocess_text(self, text: list):
        if not isinstance(text, list):
            text = [text]
        functors_pos = {'CONJ', 'ADV-PRO', 'CC', 'PR', 'CD', 'S-PRO', 'NONLEX'}
        def stem(x): return [self.stemmer.stem(y) for y in x]
        for i in range(len(text)):
            text[i] = nltk.word_tokenize(text[i], language='russian')
            text[i] = [word for word, pos in nltk.pos_tag(text[i], lang='rus')
                       if pos not in functors_pos]
            text[i] = ' '.join(stem(text[i]))
        return text

    def preprocessed_text_to_vec(self, text):
        return self.count_vect.transform(text)

    def build_model(self):
        X_train, Y_train = self.data.document_data, self.data.class_index_document_data
        X_train = self.count_vect.fit_transform(X_train)
        t = time.time()
        self.model = SVC(
            C=1,
            kernel='linear',
            gamma='auto',
            random_state=42).fit(
            X_train,
            Y_train)  # 0.8953009068425392
        print(
            time.time() - t,
            'Build model time with data shape: ',
            len(Y_train))

    def predict(self, text: list):
        if self.model is None:
            self.build_model()
        vectorized_text = self.preprocessed_text_to_vec(
            self.preprocess_text(text))
        predict = self.model.predict(vectorized_text)
        result = []
        for res in predict:
            result.append(self.data.index_name[res])
        return result

    def add_classes(self, clss: list):
        self.data.add_classes(clss)

    def add_data_with_preprocessing(self, val, clss):
        cal = self.preprocess_text(val)
        self.data.add_data(clss, val)
        self.build_model()

    def add_data_without_preprocessing(self, val, clss):
        self.data.add_data(clss, val)
        self.build_model()
