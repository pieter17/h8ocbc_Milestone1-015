from flask import make_response, abort
from config import db
from models import Movies, MoviesSchema, Directors


def filter_list(argument, limit):
    return Movies.query.order_by(argument).all(
    ) if limit < 1 else Movies.query.order_by(argument).limit(limit)


def read_all(limit=0, order_by='title', order='asc'):
    """GET all movies list with paramaters limit, order by, and order

    Args:
        limit (int, optional): limit list of movie. Defaults to 0.
        order_by (str, optional): order movie by id, popularity, vote_average, and release_data . Defaults to 'title'.
        order (str, optional): order movie asc or desc. Defaults to 'asc'.

    Returns:
        list: list of movies
    """

    if order_by == 'release_date':
        movies = filter_list(db.desc(Movies.release_date),
                             limit) if order == 'desc' else filter_list(
                                 Movies.release_date, limit)
    elif order_by == 'popularity':
        movies = filter_list(db.desc(Movies.popularity),
                             limit) if order == 'desc' else filter_list(
                                 Movies.popularity, limit)
    elif order_by == 'vote_average':
        movies = filter_list(db.desc(Movies.vote_average),
                             limit) if order == 'desc' else filter_list(
                                 Movies.vote_average, limit)
    else:
        movies = filter_list(db.desc(Movies.title),
                             limit) if order == 'desc' else filter_list(
                                 Movies.title, limit)
    movie_schema = MoviesSchema(many=True)
    data = movie_schema.dump(movies)
    return data


def read_one(director_id, movie_id):
    """GET one specific movie by id and director id

    Args:
        director_id (int): id of director associated with
        movie_id (int): id of the movie

    Returns:
        dict: dict of the movie
    """

    movie = (Movies.query.join(Directors,
                               Directors.id == Movies.director_id).filter(
                                   Directors.id == director_id).filter(
                                       Movies.id == movie_id).one_or_none())
    if movie is not None:
        movie_schema = MoviesSchema()
        data = movie_schema.dump(movie)
        return data
    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def search_title(title, limit=0):
    """Get search query by title

    Args:
        title (string): title want to search
        limit (int, optional): number of limit of list. Defaults to 0.

    Returns:
        list: list of searched movie
    """
    movies = (Movies.query.filter(
        Movies.title.like(f"%{title}%")).all()) if limit < 1 else (
            Movies.query.filter(Movies.title.like(f"%{title}%")).limit(limit))

    if movies is not None:
        schema = MoviesSchema(many=True)
        data = schema.dump(movies)
        return data
    else:
        abort(404, f"Movie not found")


def create(director_id, movie):
    """POST or create a new movie

    Args:
        director_id (int): id of director associated with
        movie (dict): object of new movie

    Returns:
        dict: dict of new movie
    """

    director = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    if director is None:
        abort(404, f"Director not found for Id: {director_id}")

    schema = MoviesSchema()
    new_movie = schema.load(movie, session=db.session)

    director.movies.append(new_movie)
    db.session.commit()

    data = schema.dump(new_movie)
    return data, 201


def update(director_id, movie_id, movie):
    """PUT or update exsisting movie

    Args:
        director_id (int): id of director associated with
        movie_id (int): id of the movie
        movie (dict): object of edited movie

    Returns:
        dict: dict of new edited movie
    """

    update_movie = (Movies.query.filter(
        Movies.director_id == director_id).filter(
            Movies.id == movie_id).one_or_none())

    if update_movie is not None:
        schema = MoviesSchema()
        update = schema.load(movie, session=db.session)
        update.director_id = update_movie.director_id
        update.id = update_movie.id
        db.session.merge(update)
        db.session.commit()
        data = schema.dump(update_movie)

        return data, 200

    else:
        abort(404, f"Movie not found for Id: {movie_id}")


def delete(director_id, movie_id):
    """DELETE a movie

    Args:
        director_id (int): id of director associated with
        movie_id (int): id of movie

    Returns:
        string: response string
    """

    movie = (Movies.query.filter(Movies.director_id == director_id).filter(
        Movies.id == movie_id).one_or_none())

    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(f"Movie {movie_id} deleted", 200)
    else:
        abort(404, f"Movie not found for Id: {movie_id}")
