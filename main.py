# Programmer: Colin Joss
# Last date updated: 3-19-2021
# Description: Pulls a review data from Yelp and exports it to as csv file.

import requests
import re
from bs4 import BeautifulSoup as Bs
import pandas as pd


def load_webpage(base_url):
    """Accepts a url from the user. Returns the website as a soup object.
    Otherwise, an error halts execution."""
    if 'https://www.yelp.com/' not in base_url:
        print('This program only works for Yelp reviews!')
        return False

    try:
        req = requests.get(base_url)
        return Bs(req.content, 'html.parser')
    except requests.exceptions.MissingSchema:
        print("That Yelp url doesn't exist!")
        return False


def get_restaurant_name(soup):
    """Accepts a beautiful soup object and returns the name of the restaurant on Yelp."""
    return soup.find('h1').get_text()


def get_user_name(soup_list):
    """Accepts a list of soup 'li' objects and returns a list of user names."""
    return [item.find('span', attrs={'class': 'fs-block css-m6anxm'}).get_text() for item in soup_list]


def get_user_link(soup_list):
    """Accepts a list of soup 'li' objects and returns a list of user profile links."""
    base = 'https://www.yelp.com'
    return [base + item.find('span', attrs={'class': 'fs-block css-m6anxm'}).find('a')['href'] for item in soup_list]


def get_post_date(soup_list):
    """Accepts a list of soup 'li' objects and returns a list of review post dates."""
    return [item.find('span', attrs={'class': 'css-e81eai'}).get_text() for item in soup_list]


def get_star_rating(soup_list):
    """Accepts a list of soup 'li' objects and returns a list of review star ratings."""
    return [item.find('div', attrs={'class': re.compile('star')})['aria-label'][0] for item in soup_list]


def get_review_content(soup_list):
    """Accepts a list of soup 'li' objects and returns a list of reviews as strings."""
    return [item.find('p', attrs={'class': re.compile('comment')}).get_text() for item in soup_list]


if __name__ == '__main__':
    # Pulls the data and saves a beautiful soup object
    url = str(input('Please paste the url here: '))
    soup = load_webpage(url)
    restaurant = get_restaurant_name(soup)
    review_data = soup.find_all('div', re.compile('review'))

    # Gets data from first page of reviews
    all_users = get_user_name(review_data)
    all_links = get_user_link(review_data)
    all_dates = get_post_date(review_data)
    all_ratings = get_star_rating(review_data)
    all_reviews = get_review_content(review_data)

    # Loops through remaining pages until end is reached
    for n in range(1, 10000):
        print(f'Getting data from page {n}...')
        next_page = url + f'?start={n * 10}'
        soup = load_webpage(next_page)
        review_data = soup.find_all('div', re.compile('review'))

        users = get_user_name(review_data)
        links = get_user_link(review_data)
        dates = get_post_date(review_data)
        ratings = get_star_rating(review_data)
        reviews = get_review_content(review_data)
        if not users or not links or not dates or not ratings or not reviews:
            break

        all_users += users
        all_links += links
        all_dates += dates
        all_ratings += ratings
        all_reviews += reviews

    # Saves data as dictionary and converts to Pandas dataframe
    restaurant_dict = {
        'user': all_users,
        'user profile': all_links,
        'post date': all_dates,
        'rating': all_ratings,
        'review': all_reviews
    }

    restaurant_df = pd.DataFrame(restaurant_dict,
                                 columns=['user', 'user profile', 'post date', 'rating', 'review'])

    # Removes duplicate rows from the dataframe
    restaurant_df.drop_duplicates()

    # Exports the data as a csv
    with open(f'{restaurant}.csv', 'a', newline='') as outfile:
        restaurant_df.to_csv(outfile)
