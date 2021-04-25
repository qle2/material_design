
"""
Main Objective: Get price + reviews + Review ratings + Ingredients from page from WALMART
"""
import re  # regex
import time
import pandas as pd
from selenium import webdriver  # browser
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


# def get_reviews(number, browser):
#     """
#     Objective: Get Reviews
#     :param number:
#     :param browser:
#     :return:
#     """
#     print('getting reviews...')
#     # go to review iteration page
#     review_url = 'https://www.walmart.com/reviews/product/' + str(number)
#     print('searching url: ' + review_url)
#     browser.get(review_url)
#
#     # start with an assumption that there are multiple pages of reviews
#     button_found = True
#     dictionary_list = []
#     # begin iteration and escape loop when the button is not found
#     counter = 1
#     while button_found is True:
#         WebDriverWait(browser, 10)  # allow some time for the page to load and not overload Walmart
#         print('page #: ', counter, ' of product ', number)
#         # start by trying to get any reviews on the page
#
#         try:
#             xpath = '//div[@class="Grid ReviewList-content"]//div//div[@class="review"]'
#             reviews = browser.find_elements_by_xpath(xpath)
#
#         except NoSuchElementException:
#             reviews = []
#
#         if len(reviews) != 0:  # if there are review elements
#             print(len(reviews))
#             for review_element in reviews:
#                 try:
#                     # desired output : {title: ____, body: _____, star: #, date: _/_/_, promotion: T/F}
#                     title, body, star, date = get_info(review_element)
#                     promo = get_promotion(body)
#
#                     print('review info: ', title, body, star, date, promo)
#
#                     dictionary_list.append({'title': title, 'body': body, 'star': star,
#                                             'date': date, 'promotion': promo})
#                 except StaleElementReferenceException:
#                     continue  # it grabs too many elements and lists the extra as stale for some reason....
#
#         # WebDriverWait(browser, 1)  # in case extra wait is needed
#
#         # try to select button
#         try:
#             # WebDriverWait(browser, 15, ignored_exceptions=StaleElementReferenceException).until(
#             #     EC.presence_of_element_located(
#             #         (
#             #             By.XPATH, "//button[@class='paginator-btn paginator-btn-next']")),
#             # )
#
#             # see if a "next page" button exists
#             next_button = browser.find_element_by_xpath("//button[@class='paginator-btn paginator-btn-next']")
#             # navigate to the next page
#             next_button.click()
#         except NoSuchElementException:
#             button_found = False
#
#         # -----
#         # TEST PAGE LIMITER TO BE DELETED
#         # if counter > 2:
#         #     button_found = False
#         # -----
#         counter = counter + 1
#         if counter % 10 == 0:
#             WebDriverWait(browser, 10)  # 10 second timeout every 10 pages
#         else:
#             WebDriverWait(browser, 1)  # otherwise just wait 1 second
#
#     df = pd.DataFrame(dictionary_list)
#     file_name = r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites\walmart' \
#                 r'\completed_products\\' + str(number) + '_reviews.csv '
#     print('data frame of reviews being printed to: \n', file_name)
#     df.to_csv(file_name, index=False)


def overview_dict(number, name, browser):
    """
    Objective: Get price + Number of review ratings for each rating
    :param number: Product id
    :param name: Product name
    :param browser: URL
    :return:
    """
    WebDriverWait(browser, 10)
    try:
        # print("here2?")
        WebDriverWait(browser, 15, ignored_exceptions=StaleElementReferenceException).until(
            ec.presence_of_element_located(
                (By.XPATH, '//div[@class="ReviewHistogram ReviewsHeader-filter-wyr"]//div//span[@class="font-normal"]')),
        )
        # print("here3?")
        star_rating_list_raw = browser.find_elements_by_xpath(
            '//div[@class="ReviewHistogram ReviewsHeader-filter-wyr"]//div//span[@class="font-normal"]')
        # print(star_rating_list_raw)
        star = [rating.text for rating in star_rating_list_raw]
        # print("star", star)
    except NoSuchElementException:
        try:
            WebDriverWait(browser, 15, ignored_exceptions=StaleElementReferenceException).until(
                ec.presence_of_element_located(
                    (By.XPATH, '//div[@class="ReviewHistogram"]//div//span[@class="font-normal"]'))
            )
            star_rating_list_raw = browser.find_elements_by_xpath(
                '//div[@class="ReviewHistogram"]//div//span[@class="font-normal"]')
            star = [rating.text for rating in star_rating_list_raw]
            # print("star",star)
        except NoSuchElementException:
            star = [0, 0, 0, 0, 0]
    # print("here")
    # get the total number of reviews
    totrev = browser.find_element_by_xpath('//span[@class="stars-reviews-count-node"]').text
    try:
        rev_search = re.search('\d+', totrev)
        revs = rev_search.group(0)
    except AttributeError:
        revs = 0

    # check if the price is a single number or a range
    try:
        xpath = '//div[@class="prod-PriceHero"]//span[@class="hide-content display-inline-block-m"]' \
                '//span//span[@class="visuallyhidden"]'
        price = browser.find_element_by_xpath(xpath).text
    except NoSuchElementException:
        try:
            xpath = '//span//div[@class="display-inline PriceRange--section"]' \
                    '//span[@class="hide-content display-inline-block-m"]//span//span[@class="visuallyhidden"]'
            html_price_list = browser.find_elements_by_xpath(xpath)
            price = html_price_list[0].text + ' - ' + html_price_list[1].text
        except IndexError:
            price = 'UNKNOWN'

    # return {'number': number, 'name': name, 'price': price}
    return {'number': number, 'name': name, 'price': price, 'review number': revs, '5 stars': star[0],
                '4 stars': star[1], '3 stars': star[2], '2 stars': star[3], '1 star': star[4]}


def get_ingredients(number, browser):
    """
    Objective: Get ingredients
    :param number:
    :param browser:
    :return:
    """

    xpath_inactive = '//section[@class="AboutProduct AboutHealth Ingredients"]//p[./span="Inactive Ingredients: "]//span[' \
                         '@class="aboutModuleText"]'
    xpath_active = '//section[@class="AboutProduct AboutHealth Ingredients"]//p[./span="Active Ingredients: "]//span[' \
                     '@class="aboutModuleText"]'

    xpath = '//section[@class="AboutProduct AboutHealth Ingredients"]//p[./span="Ingredients: "]//span[' \
            '@class="aboutModuleText"]'

    try:
        ingredient_raw = browser.find_element_by_xpath(xpath).text

    except NoSuchElementException:
        ingredient_raw = ''

    try:
        active_raw = browser.find_element_by_xpath(xpath_active).text

    except NoSuchElementException:
        active_raw = ''

    try:
        inactive_raw = browser.find_element_by_xpath(xpath_inactive).text
    except NoSuchElementException:
        inactive_raw = ''
    active = []
    inactive = []

    ingr_list = re.findall(r'[aA]ctive [iI]ngredients?:(.+)[iI]nactive [iI]ngredients?:(.+)', ingredient_raw)
    # ingr_list = re.findall(r'ctive [iI]ngredients?:(.+)', ingredient_raw)
    # print("ingr_list", ingr_list)

    # print(ingredient_raw)
    if len(ingr_list) == 0:
        ingr_list = [ingredient_raw]
    else:
        ingr_list = [ingr_str for ingr_str in ingr_list[0]]

    for ingr in ingr_list:
        lst = ingr.split(', ')
        if ingr_list.index(ingr) == 0:
            # active ingredients
            active = lst
            inactive = []
        elif ingr_list.index(ingr) == 1:
            # inactive ingredients
            inactive = lst

    return {'number': number, 'active_from_ingredients': active,
            'inactive_from_ingredients': inactive, 'active_raw': active_raw, 'inactive_raw': inactive_raw}


def main():
    """

    Get price + reviews + Review ratings + Ingredients from page
    :return:
    """
    browser = webdriver.Firefox(executable_path=r"C:\Users\quang\material_design\scrape\geckodriver-v0.29.0-win64\geckodriver.exe")
    # webdriver.Firefox()

    # get the list of toothpastes
    good_example = '../data/scrape/good_example.csv'
    bad_example = '../data/scrape/bad_example.csv'
    all_data = '../data/scrape/need_scrape.csv'
    new_data = 'data_3_21_2021.csv'
    # r'C:\Users\17032\Desktop\Graduate_Work\MPrintOKN\PerformanceDataRepo\scraping_websites\walmart' \
    # r'\master_product_list_2020-03-30.csv '
    # df = pd.read_csv(good_example, skipinitialspace=True, quotechar='"', index_col=0)  # sep = ',\S'
    df = pd.read_csv(new_data, skipinitialspace=True, quotechar='"', index_col=0)  # sep = ',\S'

    # df = pd.read_csv(bad_example, skipinitialspace=True, quotechar='"', index_col=0)  # sep = ',\S'
    # df = pd.read_csv(all_data, skipinitialspace=True, quotechar='"', index_col=0)  # sep = ',\S'

    df.set_index('product_number', inplace=True)
    # print(df)

    overview_dict_list = []
    ingredient_dict_list = []
    # problem_children = []

    for index, row in df.iterrows():
        number = index
        name = row[0]
        link = row[1]

        try:
            # print(link)
            time.sleep(1)
            browser.get(link)
            overview = overview_dict(number, name, browser)
            # print(overview)
            # print(overview)

            overview_dict_list.append(overview)

            # ingredient file
            ingredient = get_ingredients(number, browser)
            # print(ingredient)
            ingredient_dict_list.append(ingredient)


            # get_reviews(number=number, browser=browser)

            WebDriverWait(browser, 2)

        except Exception as e:
            continue
        #     break


    overview_df = pd.DataFrame.from_records(overview_dict_list)
    overview_df.to_csv("new_datareview.csv")



if __name__ == '__main__':
    main()