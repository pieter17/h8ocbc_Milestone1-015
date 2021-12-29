from flask import make_response, abort
from config import db
from models import Directors, DirectorsSchema, Movies


def filter_list(argument, limit):
    return Directors.query.order_by(argument).all(
    ) if limit < 1 else Directors.query.order_by(argument).limit(limit)


def read_all(limit=0, order_by='id', order='asc'):
    """get all list of director data from databases with paramater 
        - limit for limit list length
        - order_by for ordering by (id,name,gender,uid, or deparment)
        - order for ordering descending or ascending

    Args:
        limit (int, optional): [limit list length]. Defaults to 0.
        order_by (str, optional): [ordering by (id,name,gender,uid, or deparment)]. Defaults to 'id'.
        order (str, optional): [ordering desc or asc]. Defaults to 'asc'.

    Returns:
        list: list of dict of director datas
    """

    if order_by == 'name':
        directors = filter_list(db.desc(Directors.name),
                                limit) if order == 'desc' else filter_list(
                                    Directors.name, limit)
    elif order_by == 'gender':
        directors = filter_list(db.desc(Directors.gender),
                                limit) if order == 'desc' else filter_list(
                                    Directors.gender, limit)
    elif order_by == 'uid':
        directors = filter_list(db.desc(Directors.uid),
                                limit) if order == 'desc' else filter_list(
                                    Directors.uid, limit)
    elif order_by == 'department':
        directors = filter_list(db.desc(Directors.department),
                                limit) if order == 'desc' else filter_list(
                                    Directors.department, limit)
    else:
        directors = filter_list(db.desc(Directors.id),
                                limit) if order == 'desc' else filter_list(
                                    Directors.id, limit)

    director_schema = DirectorsSchema(many=True)
    data = director_schema.dump(directors)
    return data


def read_one(director_id):
    """Get specific director data from the databases

    Args:
        director_id (integer): id of the director

    Returns:
        Dict: Dict of director data including movies list
    """
    director = (Directors.query.filter(
        Directors.id == director_id)).outerjoin(Movies).one_or_none()

    if director is not None:
        director_schema = DirectorsSchema()
        data = director_schema.dump(director)
        return data
    else:
        abort(404, f"Director not found for Id: {director_id}")


def search_name(name, limit=0):
    """Get search query by name

    Args:
        name (string): name to search
        limit (int, optional): number of limit search list. Defaults to 0.

    Returns:
        list: list of directors
    """

    search = "%{}%".format(name)

    directors = (Directors.query.filter(
        Directors.name.like(f'%{name}%')).outerjoin(Movies).all(
        )) if limit < 1 else (Directors.query.filter(
            Directors.name.like(f'%{name}%')).outerjoin(Movies).limit(limit))

    if directors is not None:
        director_schame = DirectorsSchema(many=True)
        data = director_schame.dump(directors)
        return data
    else:
        abort(404, f"Director not found")


def create(director):
    """Post to create new director to database

    Args:
        director (dict): object of director to add

    Returns:
        dict: dict of new director
    """

    uid = director.get('uid')

    exsisting_director = (Directors.query.filter(
        Directors.uid).filter(Directors.uid == uid).one_or_none())

    if exsisting_director is None:
        schema = DirectorsSchema()
        new_director = schema.load(director, session=db.session)

        db.session.add(new_director)
        db.session.commit()

        data = schema.dump(new_director)

        return data, 201
    else:
        abort(409, f"Directors uid {uid} exists already")


def update(director_id, director):
    """PUT or update director from database

    Args:
        director_id (integer): id of the director to update
        director (dict): object of updated director

    Returns:
        dict,status code: object of updated director, and status code
    """

    update_director = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    if update_director is not None:
        schema = DirectorsSchema()
        updated = schema.load(director, session=db.session)

        updated.id = update_director.id

        db.session.merge(updated)
        db.session.commit()

        data = schema.dump(update_director)

        return data, 200
    else:
        abort(404, f"Person not found for Id: {director_id}")


def delete(director_id):
    """DELETE director from database

    Args:
        director_id (integer): id of director to delete

    Returns:
        string: string of status
    """

    director = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {director} deleted", 200)

    else:
        abort(404, f"Director not found for Id: {director_id}")
