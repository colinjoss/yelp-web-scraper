# Programmer: Colin Joss
# Last date updated: 3-18-2021
# Description:

import requests
import re
from bs4 import BeautifulSoup as Bs
import pandas as pd


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
    return [item.find('span', attrs={'class': 'fs-block css-m6anxm'}).find('a')['href'] for item in soup_list]


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
    ul_list = soup.find_all('ul')
    li_list = ul_list[9].find_all('li')

    all_users = get_user_name(li_list)
    all_links = get_user_link(li_list)
    all_dates = get_post_date(li_list)
    all_ratings = get_star_rating(li_list)
    all_reviews = get_review_content(li_list)

    # n = 20
    # loop
    #   try:
    #   next page = url + f'?start={n}'
    #   yelp soup = load webpage (next page)

    #   users = get reviewer name (yelp soup)
    #   dates = get post date (yelp soup)
    #   ratings = get star rating (yelp soup)
    #   reviews = get reviews (yelp soup)

    #   all users += users
    #   all dates += dates
    #   all ratings += ratings
    #   all reviews += reviews

    #   except error:
    #   break loop

    # restaurant dict = { populate dictionary with accumulated data }
    # restaurant df = pandas.DataFrame(restaurant_dict, columns=['user', 'date', 'rating', 'review'])
    # restaurant df append to csv named 'restaurant name'
