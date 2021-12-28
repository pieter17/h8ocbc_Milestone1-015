import json
import random
import config
from models import Directors, DirectorsSchema, Movies

connex_app = config.connex_app
connex_app.add_api('swagger.yml')
connex_app = connex_app.app

client = connex_app.test_client()


def test_director_read_all():
    url = '/api/director?limit=3'

    response = client.get(url)
    data = json.loads(response.get_data())
    assert isinstance(data, list) is True
    assert response.status_code == 200


def test_director_read_all_limit():
    limit = 253
    url = f'/api/director?limit={limit}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert len(data) == limit


def test_director_read_one():
    director_id = 4762
    url = f'/api/director/{director_id}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data['id'] == director_id


def test_director_read_one_404():
    director_id = 1
    url = f'/api/director/{director_id}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 404
    assert isinstance(data, dict)
    assert data['title'] == "Not Found"


def test_post_director_500():
    url = '/api/director'
    mock_data_fail = {"department": ""}
    mock_request_headers = {'Content-Type': 'application/json'}

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
    url = '/api/director'
    mock_request_headers = {'Content-Type': 'application/json'}
    res = client.post(url, data=json.dumps(mock_data_director), headers=mock_request_headers)
    data = json.loads(res.get_data())
    assert res.status_code == 201
    assert isinstance(data, dict)
    assert data['name'] == mock_data_director['name']


def test_put_director():
    director = (Directors.query.filter(Directors.name == mock_data_director['name'])).outerjoin(Movies).one_or_none()
    director_schema = DirectorsSchema()
    data = director_schema.dump(director)
    mock_data_director['gender'] = 2

    url = f"/api/director/{data['id']}"
    mock_request_headers = {'Content-Type': 'application/json'}
    res = client.put(url, data=json.dumps(mock_data_director), headers=mock_request_headers)
    res_data = json.loads(res.get_data())

    assert res.status_code == 200
    assert isinstance(res_data, dict)
    assert res_data['gender'] == 2


def test_delete_director():
    director = (Directors.query.filter(Directors.name == mock_data_director['name'])).outerjoin(Movies).one_or_none()
    director_schema = DirectorsSchema()
    data = director_schema.dump(director)
    url = f"/api/director/{data['id']}"
    res = client.delete(url)
    assert res.status_code == 200


def test_movie_read_all():
    url = '/api/movie?limit=3'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert isinstance(data, list) is True
    assert response.status_code == 200


def test_movie_read_all_limit():
    limit = 322
    url = f'/api/movie?limit={322}'

    res = client.get(url)
    data = json.loads(res.get_data())

    assert res.status_code == 200
    assert len(data) == limit


def test_movie_read_one():
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
    director_id = 1
    movie_id = 123
    url = f'/api/director/{director_id}/movie/{movie_id}'

    response = client.get(url)
    data = json.loads(response.get_data())

    assert response.status_code == 404
    assert isinstance(data, dict)
    assert data['title'] == "Not Found"
