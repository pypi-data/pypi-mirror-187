"""
Module for review penalizer processing logic

Review Penalizer:
Ratings are good because they give us an impression of how many people think a movie is good or bad.
However, it does matter how many people voted.
The aim is to penalize those movies where the number of ratings is low.

Find the movie with the maximum number of ratings (out of the TOP 20 only).
This is going to be the benchmark. Compare every movie’s number of ratings to this
and penalize each of them based on the following rule:
- Every 100k deviation from the maximum translates to a point deduction of 0.1.

For example:
-   suppose that the movie with the highest number of ratings has 2.456.123 ratings.
    This means that for a given movie with 1.258.369 ratings and an IMDB review score of 9.4,
    the amount of the deduction is 1.1 and therefore the adjusted rating is 8.3.

@TODO: [X] - fix the type hinting for the movies parameter
       [X] - fix the logic for the numbber of ratings lookup
       (currently we are getting the higher review instead of the higher number of ratings)
"""
from __future__ import annotations

from typing import Any


def penalize_reviews(movies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    penalize reviews form a list of movies

    Args:
        movies (list[dict[str, Any]]): list of movies.

    Returns:
        list[dict[str, Any]]: list of penalized movies.
    """
    # get max number of reviews
    max_reviews = max(movie['votes'] for movie in movies)
    # get penalized reviews
    for movie in movies:
        # if the number of votes is None, raise an exception
        if movie['votes'] is None:
            raise ValueError('The number of reviews cannot be None or 0')
        # get the number of reviews
        else:
            review = movie['votes']
            # if the number of reviews is less than the max number of reviews then penalize
            # else keep the rating as is and set penalized to False
            if review == max_reviews:
                movie['penalized'] = False
                movie['penalized_rating'] = None
            elif review < max_reviews:  # be explicit
                # get number of reviews difference
                reviews_difference = max_reviews - review
                # get the points deduction
                points_deduction = reviews_difference / 100000 * 0.1
                # get the penalized rating and round it to 1 decimals
                penalized_rating = round(movie['rating'] - points_deduction, 1)
                # update penalized review
                movie['penalized_rating'] = penalized_rating
                movie['penalized'] = True

        # re-penalize reviews based on the oscars awards
        movie = oscar_calculation(movie)

    return movies


def oscar_calculation(movies: dict[str, Any]) -> dict[str, Any]:
    """
    re-penalize reviews based on the oscars awards

    (pseudo code)
    >>> if penalized_rating is None and oscars_won >= 0: penalized_rating = None
    >>> for 1 or 2 oscars: penalized_rating = penalized_rating + 0.3
    >>> for 3 to 5 oscars: penalized_rating = penalized_rating + 0.5
    >>> for 6 to 10 oscars: penalized_rating = penalized_rating + 1.0
    >>> for 11 or more oscars: penalized_rating = penalized_rating + 1.5
    """
    if movies['penalized'] is False:
        pass

    else:
        if movies['oscars_won'] == 0:
            return movies

        elif 1 <= movies['oscars_won'] <= 2:
            movies['penalized_rating'] += 0.3
            return movies

        elif 3 >= movies['oscars_won'] <= 5:
            movies['penalized_rating'] += 0.5
            return movies

        elif 6 >= movies['oscars_won'] <= 10:
            movies['penalized_rating'] += 1.0
            return movies

        elif movies['oscars_won'] >= 11:
            movies['penalized_rating'] += 1.5
            return movies
