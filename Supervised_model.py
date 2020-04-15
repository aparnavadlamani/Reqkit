#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from skmultilearn.problem_transform import ClassifierChain
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csr_matrix, lil_matrix
from sklearn.preprocessing import MultiLabelBinarizer

def classification_model():
    dataset_full = pd.read_csv("dataset_with_labels.csv")
    dataset = dataset_full[0:102]
    col = ['Label', 'Review']
    dataset = dataset[col]
    dataset = dataset[pd.notnull(dataset['Review'])]
    dataset.shape
    ll = []
    for s in dataset['Label']:
        l = s.split(",")
        ll.append(l)
    dataset['Label'] = ll

    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))

    def clean_text(text):
        text = BeautifulSoup(text, "lxml").text # HTML decoding
        text = text.lower() # lowercase text
        text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
        text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
        text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
        return text

    stemmer = SnowballStemmer("english")

    def stemming(sentence):
        stemSentence = ""
        for word in sentence.split():
            stem = stemmer.stem(word)
            stemSentence += stem
            stemSentence += " "
        stemSentence = stemSentence.strip()
        return stemSentence

    dataset['Review'] = dataset['Review'].apply(clean_text)
    dataset['Review'] = dataset['Review'].apply(stemming)
    multilabel_binarizer = MultiLabelBinarizer()
    multilabel_binarizer.fit_transform(dataset['Label'])
    y = multilabel_binarizer.transform(dataset['Label'])
    for idx, label in enumerate(multilabel_binarizer.classes_):
        dataset[label] = y[:,idx]
    rest_dataset = dataset_full[102:]
    train_text = dataset['Review'].values.astype('U')
    test_text = rest_dataset['Review'].values.astype('U')
    vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2', max_features=10000)
    vectorizer.fit(train_text)
    vectorizer.fit(test_text)
    x_train = vectorizer.transform(train_text)
    y_train = dataset.drop(labels=['Label', 'Review'], axis=1)
    x_test = vectorizer.transform(test_text)
    selected_labels = y_train.columns[y_train.sum(axis = 0, skipna = True) > 0].tolist()
    y_train = y_train.filter(selected_labels, axis=1)
    cc_classifier = ClassifierChain(LogisticRegression(solver='lbfgs'))
    cc_classifier.fit(x_train, y_train)
    cc_predictions_proba = cc_classifier.predict_proba(x_test)
    t = 47
    y_pred_new = (cc_predictions_proba >= t/100).astype(int)
    #print(y_pred_new)
    y_train1 = lil_matrix(y_train).toarray()
    label_nums = {0:"Compatibility Issue", 1:"Feature Request", 2:"Functional Complaint", 3:"Network Problem", 4:"Resource Heavy", 5:"Uninteresting Comment", 6:"Update Issue", 7:"User Interface"}
    offset = 103
    y_pred = lil_matrix(y_pred_new).toarray()
    i=0
    ll = []
    for i in range(738):
        #print(i+103)
        #print(rest_dataset[1][i+103])
        #print(y_pred[i])
        j=0
        l = []
        for j in range(8):
            #print(j)
            if(y_pred[i][j]==1):
                #print(label_nums[j])
                str = label_nums[j]
                l.append(str)
        ll.append(l)
    rest_dataset['Label'] = ll
    dataset_full.to_csv("dataset_output.csv")

