from pandas.errors import EmptyDataError

from review_featurization.TFIDFreviews import ReviewArray
import pandas as pd
import re
from os import listdir


# file_path = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites\walmart' \
#             r'\completed_products\895353_reviews.csv '
# product_number = '895353'
# file_df = pd.read_csv(file_path)
#
# product_ele = ReviewArray(file_df)
# product_tfidf = product_ele.get_tfidf()
# product_df = pd.DataFrame(product_tfidf)
# product_df = product_df.transpose()  # columns are now the words, rows are sentences
#
# print(product_df)
# =====================================================================================================================


out_dir = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\review_featurization' \
         r'\tfidf_toothpaste_revs-bod_noStopWords'
completed = [f for f in listdir(out_dir)]
tmp = []
for file in completed:
    num = re.search('\d+', file).group(0)
    tmp.append(num)
completed = tmp
del tmp

my_dir = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites\walmart' \
         r'\completed_products'
product_file_list = [f for f in listdir(my_dir)]

for file in product_file_list:
    num = re.search('\d+', file).group(0)
    if str(num) not in completed:
        print(num)
        file_path = my_dir+'\\'+file
        # print(file_path)
        # break
        try:
            file_df = pd.read_csv(file_path)
            product_ele = ReviewArray(file_df)
            product_tfidf = product_ele.get_tfidf()
            product_df = pd.DataFrame(product_tfidf)
            product_df = product_df.transpose()
            out_file_path = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\review_featurization' \
                            r'\tfidf_toothpaste_revs-bod_noStopWords\\' + num + '_rev-tfidf.csv '
            product_df.to_csv(out_file_path, index=False)
        except EmptyDataError:
            print('empty file, number: ' + str(num))
        finally:
            completed.append(str(num))
