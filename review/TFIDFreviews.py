"""
Acquire TFIDF values given a product's list of reviews

Author: Kaitlin Kay
Start Date: 4/7/2020

import structure should be a pandas dataframe with the columns:
title,  body,   star,   date,   promotion

credit: https://towardsdatascience.com/text-summarization-using-tf-idf-e64a0644ace3
"""

# IMPORTS
import pandas as pd
import math
import string
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from autocorrect import Speller
import numpy as np

# FUNCTIONS
def _create_frequency_matrix(reviews, spell):
    frequency_matrix = {}
    stopWords = set(stopwords.words("english"))
    ps = PorterStemmer()

    for rev in reviews:
        print(rev)
        try:
            if '[This review was collected as part of a promotion.]' in rev:
                rev = rev.replace('[This review was collected as part of a promotion.]', '')

            print('passed')
            freq_table = {}
            rev = rev.translate(str.maketrans("", "", string.punctuation))
            words = word_tokenize(rev)
            for word in words:
                word = word.lower()
                word = spell(word)

                if word in stopWords:
                    continue

                word = ps.stem(word)

                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

            frequency_matrix[rev[:15]] = freq_table
        except TypeError:  # error thrown if value is NaN
            print('failed')
            continue

    return frequency_matrix


def _create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def _create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


class ReviewArray:
    df = pd.DataFrame()

    def __init__(self, df):
        if isinstance(df, pd.DataFrame) and df.columns.values.tolist() == ['title', 'body',
                                                                           'star', 'date', 'promotion']:
            self.df = df
        else:
            print('pandas dataframe not supplied or headers are incorrect', '\n',
                  'headers should be : title, body, star, date, promotion')

    def get_tfidf(self):
        df = self.df
        reviews = df['body']
        spell = Speller(lang='en')
        freq_matrix = _create_frequency_matrix(reviews=reviews, spell=spell)
        tf_matrix = _create_tf_matrix(freq_matrix)
        count_doc_per_words = _create_documents_per_words(freq_matrix)
        idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents=len(reviews))
        tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
        return tf_idf_matrix
