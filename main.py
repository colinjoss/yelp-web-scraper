# Programmer: Colin Joss
# Last date updated: 3-18-2021
# Description:

import requests
import re
from bs4 import BeautifulSoup as Bs
import pandas as pd


# func load webpage as soup (url)
#   accepts url string, gets request, converts to soup object, else error

# func get reviewer name (yelp soup object)
#   accepts yelp soup object and returns a list of user names

# func get review date (yelp soup object)
#   accepts yelp soup object and returns a list of dates

# func get star rating (yelp soup object)
#   accepts yelp soup object and returns a list of int star ratings

# func get reviews (yelp soup object)
#   accepts yelp soup object and returns a list of reviews

# func get restaurant name (yelp soup object)
#   accepts yelp soup object and returns the restaurant name as a string


if __name__ == '__main__':
    pass

    # url = str ( input ( 'please paste the url here' )
    # yelp soup = load webpage (url)
    # restaurant = get restaurant name (yelp soup)

    # all users = get user name (yelp soup)
    # all dates = get post date (yelp soup)
    # all ratings = get star rating (yelp soup)
    # all reviews = get reviews (yelp soup)

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
