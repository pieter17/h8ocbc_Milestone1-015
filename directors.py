from flask import make_response, abort
from config import db
from models import Directors, DirectorsSchema, Movies


def filter_list(argument, limit):
    return Directors.query.order_by(argument).all(
    ) if limit < 1 else Directors.query.order_by(argument).limit(limit)


def read_all(limit=0, order_by='id', order='asc'):
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
    director = (Directors.query.filter(
        Directors.id == director_id)).outerjoin(Movies).one_or_none()

    if director is not None:
        director_schema = DirectorsSchema()
        data = director_schema.dump(director)
        return data
    else:
        abort(404, f"Director not found for Id: {director_id}")


def create(director):
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
    director = Directors.query.filter(
        Directors.id == director_id).one_or_none()

    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Directors {director} deleted", 200)

    else:
        abort(404, f"Person not found for Id: {director_id}")
