# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1 : ========================================================

# first we need to get a list of products that have a similar number of reviews. This is important when considering
# tfidf since the second part of the function is number of documents - ie the number of reviews in our case

overview_path = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites\walmart' \
                r'\toothpaste_overview_2020-04-01.csv '
overview_df = pd.read_csv(overview_path)
overview_df.set_index('number', inplace=True)

# first let's fix the review number variable since the script picked up the wrong ones
# counter = 0
for number, row in overview_df.iterrows():
    # print('product number: ' + str(number) + '\t (' + str(counter) + '/5)')
    stars = row[-5:]
    revs = 0
    for star in stars:
        # print(star)
        revs = revs + star
    # print('total reviews: '+ str(revs))
    row[2] = revs
    overview_df.at[number, 'review number'] = revs
    # print('new dataframe row: \n', overview_df.loc[number])
    # if counter > 4:
    #     break
    # counter = counter + 1

# # next we should sort based off review number
# overview_df.sort_values(by=['review number'])
#
# now lets see what the most common review number is
most_common = overview_df['review number'].value_counts()  # .max()
print(most_common)
#
# since only getting products with this number of reviews is pretty limiting, we should consider getting a range of
# products within an interval of review numbers - I have chosen arbitrartily +/-25, I think this number would give
# an appropriate range for similarly reviewed products
print('the max value is :', most_common.max())
max_1 = most_common.max() + 25
min_1 = most_common.max() - 25

# now to extract out the relevant products
ranged_df_1 = pd.DataFrame(columns=list(overview_df.columns.values))
for number, row in overview_df.iterrows():
    if min_1 <= row[2] <= max_1:
        ranged_df_1.loc[number] = overview_df.loc[number]
ranged_df_1.drop(['name', 'price'], axis=1, inplace=True)
print(ranged_df_1)

# I am going to make a second one because I want to work in a slightly larger range to see if I can increase
# the population I am working with
max_2 = 1500
min_2 = 500
ranged_df_2 = pd.DataFrame(columns=list(overview_df.columns.values))
for number, row in overview_df.iterrows():
    if min_2 <= row[2] <= max_2:
        ranged_df_2.loc[number] = overview_df.loc[number]
ranged_df_2.drop(['name', 'price'], axis=1, inplace=True)
print(ranged_df_2)

# so now we have two possible lists of products that we can analyze the tfidf values of with varying confidence on their
# ranges relating to their review counts

# Step 2: ========================================================

# first we need to decide on the word(s) to analyse the tfidf values of... we can print the most common among all
# products within the toothpaste category
top_tfidf_path = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\review_featurization' \
                 r'\top_tfidf_toothpaste.csv '
top_tfidf_df = pd.read_csv(top_tfidf_path)
top_tfidf_df.set_index('number', inplace=True)
nan_count = top_tfidf_df.isnull().sum(axis=0)
nan_count = nan_count.sort_values()
print(nan_count)

# we now have a descending list of words whose tfidf values were high across products in the toothpaste category
# from this we should choose a set of words to compare across our two populations of products

# lets take the top 25
top_25 = nan_count[:25]
print(top_25)
# this seems to provide a good range on occurrences, though I am still concerned about the total number of words

# Step 3: ========================================================

# now we want to show the variation on these words across our two product lists
# it would also be helpful to sort the products based on their average star rating
#   image attached shows the ideal output though parameters such as which and how many words to show per figure are
#   not currently decided upon

# start with sorting the dataframes
for number, row in ranged_df_1.iterrows():
    # add new column with the average star rating
    star_rating = 0
    stars = row[-5:]
    value = 5
    for star in stars:
        star_rating = star_rating + (value * star)
        value = value - 1
    star_rating = star_rating / row[0]
    ranged_df_1.at[number, 'avg star'] = star_rating
ranged_df_1.sort_values(by=['avg star'], inplace=True)
print(ranged_df_1)

for number, row in ranged_df_2.iterrows():
    # add new column with the average star rating
    star_rating = 0
    stars = row[-5:]
    value = 5
    for star in stars:
        star_rating = star_rating + (value * star)
        value = value - 1
    star_rating = star_rating / row[0]
    ranged_df_2.at[number, 'avg star'] = star_rating
ranged_df_2.sort_values(by=['avg star'], inplace=True)
print(ranged_df_2)

# now that they're in order we should add the tfidf values of our list of words for each product
# for those without a value for a tfidf, we'll replace those with the value of 0
word_tuple = top_25.index
print(word_tuple, len(word_tuple))

for number, row in ranged_df_1.iterrows():
    # get the tfidf values from the tfidf array of our list of words
    try:
        for word in word_tuple:
            ranged_df_1.at[number, word] = top_tfidf_df.at[number, word]
        print(ranged_df_1.loc[number])
    except KeyError:  # for some reason some products didn't make it into the list? - might be a lack of test error
        for word in word_tuple:
            ranged_df_1.at[number, word] = np.nan
ranged_df_1.fillna(0, inplace=True)
print(ranged_df_1)

for number, row in ranged_df_2.iterrows():
    # get the tfidf values from the tfidf array of our list of words
    try:
        for word in word_tuple:
            ranged_df_2.at[number, word] = top_tfidf_df.at[number, word]
        print(ranged_df_2.loc[number])
    except KeyError:  # for some reason some products didn't make it into the list? - might be a lack of test error
        for word in word_tuple:
            ranged_df_2.at[number, word] = np.nan
ranged_df_2.fillna(0, inplace=True)
print(ranged_df_2)

# so now we have all our data, now we just need to graph it!
palette = plt.get_cmap('tab20')
pltnum = 0
drop_list = ['review number', '5 stars', '4 stars', '3 stars', '2 stars', '1 star', 'avg star']
for column in ranged_df_1.drop(drop_list, axis=1):
    pltnum += 1

    # Find the right spot on the plot
    plt.subplot(1, 1, pltnum)

    # # plot every groups, but discreet - this ended up not looking very pretty
    # for v in ranged_df_1.drop(drop_list, axis=1):
    #     plt.plot(ranged_df_1['avg star'], ranged_df_1[v], marker='', color='grey', linewidth=0.6, alpha=0.3)

    # Plot the lineplot
    plt.plot(ranged_df_1['avg star'], ranged_df_1[column], marker='', color=palette(2), linewidth=2.4, alpha=0.9, label=column)

    # Same limits for everybody!
    plt.xlim(3.5, 5)
    plt.ylim(0, 5)

    plt.title(column, loc='left', fontsize=12, fontweight=0, color='black')

    # Not ticks everywhere
    if pltnum < 7:
        plt.tick_params(labelbottom='off')
    if pltnum not in [1, 4, 7]:
        plt.tick_params(labelleft='off')

    if pltnum >= 1:
        break

# # Axis title
# plt.text(0.5, 0.02, 'products in ascending value of average star ratings', ha='center', va='center')
# plt.text(0.06, 0.5, 'TFIDF values of selected words', ha='center', va='center', rotation='vertical')

plt.show()


