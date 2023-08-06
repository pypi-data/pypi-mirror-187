"""
Module for scraping IMDB movie chart data.

The intent of this module is to scrape the IMDB movie chart data (TOP 250) https://www.imdb.com/chart/top/
and return a list of movie data objects.

The movie data objects are defined in the schema module. We will design the data structure to be
compatible with the schema module.

The IMDB movie chart data is scraped using the requests library. The data is then parsed using the
BeautifulSoup library.

@TODO: [X] - Add support for scraping the number of reviews given to a movie.
"""
from __future__ import annotations

import logging

import requests
from bs4 import BeautifulSoup

from imdb_rating_classifier.util.unpack import unpack_contents

# initialize logger
logger = logging.getLogger('imdb_rating_classifier')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    datefmt='[%Y-%m-%d][%H:%M:%S]',
)
# prints the log message to the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# html tags and attributes
IMDB_URL = 'https://www.imdb.com/chart/top/'
# the IMDB movie chart data is stored in a table with the class "lister-list"
IMDB_MOVIE_CHART_SELECTOR = 'tbody.lister-list tr'
IMDB_MOVIE_RANK_SELECTOR = 'td.titleColumn'
IMDB_MOVIE_TITLE_SELECTOR = 'td.titleColumn a'
IMDB_MOVIE_YEAR_SELECTOR = 'td.titleColumn span.secondaryInfo'
IMDB_MOVIE_RATING_SELECTOR = 'td.ratingColumn strong'  # "title" attribute of the "a" tag


class Scraper:
    """
    Class for scraping IMDB movie chart data.

    @TODO: - Add support for scraping multiple pages of the IMDB movie chart?
           - static typing to the class?
    """

    def __init__(self, number_of_movies: int, url: str = IMDB_URL):
        """
        Initialize Scraper class.

        Args:
            url (str, optional): IMDB movie chart URL. Defaults to IMDB_URL.
        """
        self.url = url
        self.number_of_movies = number_of_movies

    def scrape(self) -> list[dict]:
        """
        Scrape IMDB movie chart data and return a list of movie data objects.

        Returns:
            list[dict]: List of movie data objects.
        """
        # initialize movie chart data
        movie_chart_data = []

        # scrape IMDB movie
        logger.info('Scraping IMDB movie chart data...')
        response = unpack_contents(response=requests.get(self.url))
        # TODO: redundant code..remove?
        response.raise_for_status()

        # parse IMDB movie chart data
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_chart = soup.select(IMDB_MOVIE_CHART_SELECTOR)

        # parse movie chart data
        logger.info('Parsing IMDB movie chart data...')
        for movie in movie_chart:
            # parse the rank of the movie and remove the new line characters.
            movie_rank = movie.select_one(IMDB_MOVIE_RANK_SELECTOR).text.strip().split('.')[0]
            movie_title = movie.select_one(IMDB_MOVIE_TITLE_SELECTOR).text.strip()
            movie_year = movie.select_one(IMDB_MOVIE_YEAR_SELECTOR).text.strip()
            movie_rating = movie.select_one(IMDB_MOVIE_RATING_SELECTOR).text.strip()
            movie_votes = movie.select_one(IMDB_MOVIE_RATING_SELECTOR).get('title').split()[3]
            movie_url = movie.select_one(IMDB_MOVIE_TITLE_SELECTOR).get('href')

            # create a movie data object
            movie_data = {
                'rank': movie_rank,
                'title': movie_title,
                'year': movie_year,
                'rating': movie_rating,
                'votes': movie_votes,
                'url': movie_url,
                'penalized' : False,
            }
            # append movie data object to movie chart data
            movie_chart_data.append(movie_data)

        # clean movie chart data
        movie_chart_data = self.clean_movie_chart_data(movie_chart_data)

        return movie_chart_data[: self.number_of_movies]

    @staticmethod
    def clean_movie_chart_data(movie_chart_data: list[dict]) -> list[dict]:
        """
        Clean movie chart data.

        Args:
            movie_chart_data (list[dict]): List of movie data objects.

        Returns:
            list[dict]: List of cleaned movie data objects.
        """
        # clean movie chart data
        logger.info('Cleaning IMDB movie chart data...')
        for movie in movie_chart_data:
            # remove the parentheses from the movie year
            movie['year'] = movie['year'].replace('(', '').replace(')', '')
            # remove the comma from the number of votes
            movie['votes'] = movie['votes'].replace(',', '')
            # remove the leading slash from the movie url and append the IMDB url
            movie['url'] = movie['url'].replace('/', '', 1)
            movie['url'] = f'https://www.imdb.com/{movie["url"]}'

        return movie_chart_data


# TODO: add support for the oscars data
def get_movie_oscar_data(movie_url: str) -> int:
    """
    Get the Oscar data for a movie.

    Args:
        movie_url (str): IMDB movie URL.

    Returns:
        int: Number of Oscars won by the movie.
    """
    result = requests.get(
        movie_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/70.0.3538.77 Safari/537.36',
        },
    )
    content = result.text
    # parse the html content
    more_soup = BeautifulSoup(content, 'html.parser')
    element = more_soup.find_all(class_='ipc-metadata-list-item__label')

    # parse movie Oscar data
    try:
        extracted_text = element[6].get_text(strip=True).split()
        if extracted_text[0] == 'Won' and 'Oscar' in extracted_text[-1]:
            return int(extracted_text[1])

    except IndexError:
        pass

    return 0
