"""
this script is intended to exctract both adjectives and noun combinations using the NLTK library. This is intended
to be used for data creation to be used in machine learning scripts.

Author: Kaitlin
Date started: 5/12/2020
"""
# IMPORTS
import pandas as pd
from os import listdir
import re
from nltk import word_tokenize, PorterStemmer, pos_tag
from nltk.corpus import stopwords
from autocorrect import Speller
import math
from pandas.errors import EmptyDataError

review_file_dir = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites\walmart' \
                  r'\completed_products'
file_list = [f for f in listdir(review_file_dir)]

review_word_dict_list = []  # this will contain a list of dictionaries
# each dictionary will be of all words that a product has in its reviews
stopWords = set(stopwords.words("english"))

ps = PorterStemmer()
spell = Speller(lang='en')

for file in file_list:
    try:
        num = re.search('\d+', file).group(0)
        f_path = review_file_dir + '\\' + file
        f_df = pd.read_csv(f_path)
        prod_dict = {'product_number': num}
        for indx, row in f_df.iterrows():
            rev = row[1]
            print(rev)
            if rev == '' or pd.isna(rev) is True:
                continue
            else:
                # separate and clean
                words = word_tokenize(rev)
                words = [word.lower() for word in words]
                words = [spell(word) for word in words]
                words = [word for word in words if word not in stopWords]
                # get parts of speech
                pos = pos_tag(words)
                # get adjectives and ___ noun combinations
                for pos_tup in pos:
                    if 'JJ' in pos_tup[1]:
                        # its an adjective
                        if pos_tup[0] in prod_dict:
                            prod_dict[pos_tup[0]] += 1
                        else:
                            prod_dict[pos_tup[0]] = 1
                    elif 'NN' in pos_tup[1]:
                        current_index = pos.index(pos_tup)
                        if current_index > 0:
                            current_word = pos_tup[0]
                            previous_word = pos[current_index - 1][0]
                            word_combo = previous_word + ' ' + current_word
                            if word_combo in prod_dict:
                                prod_dict[word_combo] += 1
                            else:
                                prod_dict[word_combo] = 1
                    else:
                        continue
        review_word_dict_list.append(prod_dict)
    except EmptyDataError:
        continue
word_count_df = pd.DataFrame(review_word_dict_list)
word_count_df.set_index('product_number', inplace=True)
print(word_count_df.shape, word_count_df.head())

# rest should be the same since it's only dependent on the above dataframe ===========================================
tf_dict_list = []
word_per_prod = {}
for num, row in word_count_df.iterrows():
    tot_word_count = len(row)
    tf_dict = {'product_number': num}
    for word, val in row.items():
        # calculate term frequency
        tf = val / tot_word_count
        tf_dict.update({word: tf})

    tf_dict_list.append(tf_dict)

tf_df = pd.DataFrame(tf_dict_list)
tf_df.set_index('product_number', inplace=True)
print(tf_df.shape, '\n', tf_df.head())

for num, row in word_count_df.iterrows():
    for word, count in row.items():
        if pd.notna(count) is True:
            if word in word_per_prod:
                word_per_prod[word] += 1
            else:
                word_per_prod[word] = 1

print(word_per_prod)

idf_dict_list = []
tot_prods = len(word_count_df.index)
for num, row in word_count_df.iterrows():
    tot_word_count = len(row)
    idf_dict = {'product_number': num}
    for word, val in row.items():
        idf = math.log10(tot_prods/float(word_per_prod[word]))
        idf_dict.update({word: idf})

    idf_dict_list.append(idf_dict)
idf_df = pd.DataFrame(idf_dict_list)
idf_df.set_index('product_number', inplace=True)
print(idf_df.shape, '\n', idf_df.head())

tf_idf_dict_list = []
for (num_tf, row_tf), (num_idf, row_idf) in zip(tf_df.iterrows(), idf_df.iterrows()):
    tf_idf_dict = {'product_number': num_tf}
    for (word_tf, tf), (word_idf, idf) in zip(row_tf.items(), row_idf.items()):
        tf_idf = float(tf * idf)
        tf_idf_dict.update({word_tf: tf_idf})
    tf_idf_dict_list.append(tf_idf_dict)

tf_idf_df = pd.DataFrame(tf_idf_dict_list)
tf_idf_df.set_index('product_number', inplace=True)
print(tf_idf_df.shape, '\n', tf_idf_df.head())
# max_df = tf_idf_df.max(axis=1)
# print(max_df)

tf_idf_df.to_csv('toothpaste_modified_tfidf_5-12-2020.csv')
