import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

tfidf_df = pd.read_csv(r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\review_featurization'
                       r'\toothpaste_product_tfidf_4-24-2020.csv')
overview_df = pd.read_csv(r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites'
                          r'\walmart\toothpaste_overview_2020-04-01.csv')

tfidf_df.set_index('product_number', inplace=True)
overview_df.set_index('number', inplace=True)

print(tfidf_df.head())

for num, row in tfidf_df.iterrows():
    overview_row = overview_df.loc[[num], ['5 stars','4 stars','3 stars','2 stars','1 star']]
    val, i, avg_star, rev_count = 5, 0, 0, 0
    while i < 5:
        rev = overview_row.iloc[0][i]
        avg_star += val * rev
        rev_count += rev
        i += 1
        val -= 1
    avg_star = avg_star / rev_count

    tfidf_df.loc[num, 'avg_star'] = avg_star

print(tfidf_df['avg_star'])

plt_df = tfidf_df.copy(deep=True)
plt_df.reset_index(drop=True, inplace=True)
plt_df.set_index('avg_star', inplace=True)
plt_df.sort_index(inplace=True)
max_val = plt_df.values.max()
column_list = list(plt_df.columns.values)
column_list = column_list[:50]
plt_df = plt_df.loc[:, column_list]
num_na = int(50 * 0.8)
plt_df = plt_df.dropna(thresh=num_na)
print('plot dataframe: ', plt_df)

ax = sns.heatmap(plt_df, cmap='viridis')
plt.show()
