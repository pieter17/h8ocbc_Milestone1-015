import json
import random
import config
from models import Directors, DirectorsSchema, Movies, MoviesSchema

connex_app = config.connex_app
connex_app.add_api('swagger.yml')
connex_app = connex_app.app

client = connex_app.test_client()

mock_request_headers = {'Content-Type': 'application/json'}


def test_director_read_all():
    """
    test GET director
    """

    url = '/api/director?limit=3'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, list) is True
    assert response.status_code == 200


def test_director_read_all_limit():
    """
    test get director with limit
    """
    limit = 253
    url = f'/api/director?limit={limit}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert len(data) == limit


def test_director_read_one():
    """
    test get director with id
    """
    director_id = 4762
    url = f'/api/director/{director_id}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['id'] == director_id


def test_director_read_one_404():
    """
    test get with wrong value
    """
    director_id = 1
    url = f'/api/director/{director_id}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 404
    assert isinstance(data, dict)
    assert data['title'] == "Not Found"


def test_post_director_500():
    """
    test post with wrong value
    """
    url = '/api/director'
    mock_data_fail = {"department": ""}

    res = client.post(url,
                      data=json.dumps(mock_data_fail),
                      headers=mock_request_headers)
    assert res.status_code == 500


mock_data_director = {
    "department": "Directing",
    "gender": 0,
    "name": "TestName123",
    "uid": random.randint(11111, 999999)
}


def test_post_director_create():
    """
    test post director
    """
    url = '/api/director'

    res = client.post(url,
                      data=json.dumps(mock_data_director),
                      headers=mock_request_headers)
    data = json.loads(res.get_data())
    assert res.status_code == 201
    assert isinstance(data, dict)
    assert data['name'] == mock_data_director['name']


def test_put_director():
    """
    test put director
    """
    director = (Directors.query.filter(
        Directors.name == mock_data_director['name'])
    ).outerjoin(Movies).one_or_none()
    director_schema = DirectorsSchema()
    data = director_schema.dump(director)
    mock_data_director['gender'] = 2

    url = f"/api/director/{data['id']}"
    res = client.put(url,
                     data=json.dumps(mock_data_director),
                     headers=mock_request_headers)
    res_data = json.loads(res.get_data())

    assert res.status_code == 200
    assert isinstance(res_data, dict)
    assert res_data['gender'] == 2


def test_delete_director():
    """
    test delete director
    """
    director = (Directors.query.filter(
        Directors.name == mock_data_director['name'])
    ).outerjoin(Movies).one_or_none()
    director_schema = DirectorsSchema()
    data = director_schema.dump(director)
    url = f"/api/director/{data['id']}"
    res = client.delete(url)
    assert res.status_code == 200


###################################################################################################################


def test_movie_read_all():
    """
    test get movie
    """
    url = '/api/movie?limit=3'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert isinstance(data, list) is True
    assert response.status_code == 200


def test_movie_read_all_limit():
    """
    test get movie with limit
    """
    limit = 322
    url = f'/api/movie?limit={322}'

    res = client.get(url)
    data = json.loads(res.get_data())

    assert res.status_code == 200
    assert len(data) == limit


def test_movie_read_one():
    """
    test get movie with id
    """
    director_id = 4762
    movie_id = 43597
    url = f'/api/director/{director_id}/movie/{movie_id}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['id'] == movie_id
    assert data['directors']['id'] == director_id


def test_movie_read_one_404():
    """
    test get movie with wrong id
    """
    director_id = 1
    movie_id = 123
    url = f'/api/director/{director_id}/movie/{movie_id}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 404
    assert isinstance(data, dict)
    assert data['title'] == "Not Found"


mock_data_movie = {
    "budget": 11000,
    "original_title": "Iron Man 21",
    "overview": "Ironman 21",
    "popularity": 10,
    "release_date": "2010-10-10",
    "revenue": 1100000,
    "tagline": "Iron man 21",
    "title": "Iron Man 21",
    "uid": 112233,
    "vote_average": 10,
    "vote_count": 10
}


def test_post_movie_create():
    """
    test post movie
    """
    director_id = 4768
    url = f'/api/movie/{director_id}/movie'
    res = client.post(url,
                      data=json.dumps(mock_data_movie),
                      headers=mock_request_headers)
    data = json.loads(res.get_data())
    assert res.status_code == 201
    assert isinstance(data, dict)
    assert data['title'] == mock_data_movie['title']


def test_put_movie():
    """
    test put movie
    """
    director_id = 4768
    movie = (Movies.query.filter(
        Movies.title == mock_data_movie['title']).filter(
        Movies.uid == mock_data_movie['uid']).one_or_none())
    movie_schema = MoviesSchema()
    data = movie_schema.dump(movie)
    mock_data_movie['popularity'] = 2

    url = f"/api/director/{director_id}/movie/{data['id']}"
    res = client.put(url,
                     data=json.dumps(mock_data_movie),
                     headers=mock_request_headers)
    res_data = json.loads(res.get_data())

    assert res.status_code == 200
    assert isinstance(res_data, dict)
    assert res_data['popularity'] == 2


def test_delete_movie():
    """
    test delete movie
    """
    director_id = 4768
    movie = (Movies.query.filter(
        Movies.title == mock_data_movie['title']).filter(
        Movies.uid == mock_data_movie['uid']).one_or_none())
    movie_schema = MoviesSchema()
    data = movie_schema.dump(movie)
    url = f"/api/director/{director_id}/movie/{data['id']}"
    res = client.delete(url)
    assert res.status_code == 200
