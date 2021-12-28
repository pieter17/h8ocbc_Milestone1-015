from config import db, ma
from marshmallow import fields


class Directors(db.Model):
    __tablename__ = 'directors'
    name = db.Column(db.String, index=True)
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.String)
    # don't know abot this one
    movies = db.relationship('Movies',
                             backref='directors',
                             lazy=True,
                             cascade='all, delete, delete-orphan',
                             single_parent=True)


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.String)
    revenue = db.Column(db.Integer)
    title = db.Column(db.String)
    vote_average = db.Column(db.REAL)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.String)
    tagline = db.Column(db.String)
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))


class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Directors
        include_relationships = True
        load_instance = True

    movies = fields.Nested('DirectorsMoviesSchema', default=[], many=True)


class DirectorsMoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int()
    release_date = fields.String()
    revenue = fields.Int()
    title = fields.Str()
    vote_average = fields.Float()
    vote_count = fields.Int()
    overview = fields.Str()
    tagline = fields.Str()
    uid = fields.Int()
    director_id = fields.Int()


class MoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        include_relationships = True
        load_instance = True

    directors = fields.Nested("MoviesDirectorsSchema", default=None)


class MoviesDirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    name = fields.Str()
    id = fields.Int()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()
