# Programmer: Colin Joss
# Last date updated: 3-18-2021
# Description:

import requests
import re
from bs4 import BeautifulSoup as Bs
import pandas as pd
import csv


def load_webpage(base_url):
    """Accepts a url from the user. Returns the website as a soup object.
    Otherwise, an error halts execution."""
    try:
        req = requests.get(base_url)
        return Bs(req.content, 'html.parser')
    except requests.exceptions.MissingSchema:
        print("That url doesn't exist!")


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
    url = str(input('Please paste the url here: '))
    soup = load_webpage(url)
    restaurant = get_restaurant_name(soup)
    review_data = soup.find_all('div', re.compile('review'))

    all_users = get_user_name(review_data)
    all_links = get_user_link(review_data)
    all_dates = get_post_date(review_data)
    all_ratings = get_star_rating(review_data)
    all_reviews = get_review_content(review_data)

    n = 10
    while True:
        next_page = url + f'?start={n}'
        print(next_page)
        soup = load_webpage(next_page)
        ul_list = soup.find_all('ul')
        li_list = ul_list[9].find_all('li')

        users = get_user_name(li_list)
        links = get_user_link(li_list)
        dates = get_post_date(li_list)
        ratings = get_star_rating(li_list)
        reviews = get_review_content(li_list)
        if not users or not links or not dates or not ratings or not reviews:
            break

        all_users += users
        all_links += links
        all_dates += dates
        all_ratings += ratings
        all_reviews += reviews
        n += 10

    restaurant_dict = {
        'user': all_users,
        'user profile': all_links,
        'post date': all_dates,
        'rating': all_ratings,
        'review': all_reviews
    }

    restaurant_df = pd.DataFrame(restaurant_dict,
                                 columns=['user', 'user profile', 'post date', 'rating', 'review'])
    with open(f'{restaurant}.csv', 'a', newline='') as outfile:
        restaurant_df.to_csv(outfile)
