#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
import pandas as pd
import re
import heapq
from sklearn.preprocessing import MultiLabelBinarizer
BAD_SYMBOLS_RE = re.compile("[ /(){}\[\]\|@;']")
def redundancy_reduction():
    dataset = pd.read_csv("dataset_output.csv")
    dataset = dataset[['Label', 'Review']]
    ll = []
    for s in dataset['Label']:
        s = BAD_SYMBOLS_RE.sub('', s)
        l = s.split(",")
        ll.append(l)
    dataset['Label'] = ll
    multilabel_binarizer = MultiLabelBinarizer()
    multilabel_binarizer.fit_transform(dataset['Label'])
    y = multilabel_binarizer.transform(dataset['Label'])
    for idx, label in enumerate(multilabel_binarizer.classes_):
        dataset[label] = y[:,idx]
    ls = []
    fc = list(dataset.loc[dataset['FunctionalComplaint'] == 1].Review)
    ui = list(dataset.loc[dataset['UserInterface'] == 1].Review)
    updatei = list(dataset.loc[dataset['UpdateIssue'] == 1].Review)
    ci = list(dataset.loc[dataset['CompatibilityIssue'] == 1].Review)
    fr = list(dataset.loc[dataset['FeatureRequest'] == 1].Review)
    np = list(dataset.loc[dataset['NetworkProblem'] == 1].Review)
    rh = list(dataset.loc[dataset['ResourceHeavy'] == 1].Review)
    ls = [fc, ui, updatei, ci, fr, np, rh]
    index = ["Functional Complaint", "User Interface", "Update Issue", "Compatibility Issue", "Feature Request", "Network Problem", "Resource Heavy"]
    def summarization(article_text):
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        return summary
    def combine_reviews(l):
        article_text = ""
        for s in l:
            article_text += s
        return article_text
    summaries = {}
    for i, l in zip(index, ls):
        summaries[i]=summarization(combine_reviews(l))
    return summaries

