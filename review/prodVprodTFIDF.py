from pandas.errors import EmptyDataError
from review_featurization.TFIDFreviews import ReviewArray
import pandas as pd
import re
from os import listdir


def prod_row(num, df):
    master = {'number': num,
              'title': '',
              'body': '',
              'star': 0,
              'date': pd.np.nan,
              'promotion': pd.np.nan}
    for index, row in df.iterrows():
        title, body, star = row[0], row[1], row[2]
        if pd.isna(title) is False:
            title = ' ' + title
            master['title'] += title
        if pd.isna(body) is False:
            body = ' ' + body
            master['body'] += body
        master['star'] += star
    revs = len(df['star'])
    master['star'] = master['star'] / revs
    return master


my_dir = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites\walmart' \
         r'\completed_products'
product_file_list = [f for f in listdir(my_dir)]

prod_dict_list = []

for file in product_file_list:
    prodnum = re.search('\d+', file).group(0)
    print(prodnum)
    file_path = my_dir + '\\' + file
    try:
        file_df = pd.read_csv(file_path)
        prod_dict = prod_row(num=prodnum, df=file_df)
        prod_dict_list.append(prod_dict)
    except EmptyDataError:
        print('empty file, number: ' + str(prodnum))

prod_raw_df = pd.DataFrame(prod_dict_list)
prod_raw_df.to_csv('toothpaste_reviewSUM.csv')
# product_num_column = prod_raw_df['number']
# prod_nonum_df = prod_raw_df.drop(columns=['number'])
#
# prod_nonum_df.reindex()
# product_num_column.reindex()
#
# cat_ele = ReviewArray(prod_nonum_df)
# cat_tfidf = cat_ele.get_tfidf()
# prod_df = pd.DataFrame(cat_tfidf)
# prod_df = prod_df.transpose()
#
# prod_df.to_csv('nonnum_category_TFIDF.csv')
# product_num_column.to_csv('numcolumn_df.csv')
#
# prod_df.join(product_num_column)
#
# prod_df.set_index('number', inplace=True)
# print(prod_df)
# prod_df.to_csv('category_TFIDF.csv')
