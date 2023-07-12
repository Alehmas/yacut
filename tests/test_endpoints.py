import pytest

from yacut.models import URL_map

py_url = 'https://www.python.org'


def test_create_id(client):
    got = client.post('/api/id/', json={
        'url': py_url,
        'custom_id': 'py',
    })
    assert got.status_code == 201, (
        'When creating a short link, status code 201 should be returned'
    )
    assert list(got.json.keys()) == ['short_link', 'url'], (
        'When creating a short link, the response must contain the keys `url, short_link`'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/py',
    }, 'When creating a short link, the body of the API response is different than expected.'


def test_create_empty_body(client):
    try:
        got = client.post('/api/id/')
    except Exception:
        raise AssertionError('If no information is passed in the body of the request, throw an exception.')
    assert got.status_code == 400, (
        'An empty POST request to the `/api/id/` endpoint should return a status code of 400.'
    )
    assert list(got.json.keys()) == ['message'], (
        'The response to an empty POST request to the `/api/id/` endpoint must contain the key `message`'
    )
    assert got.json == {'message': 'Request body missing'}, (
        'Message in response body when creating shortlink '
        'without a body in the request does not match the specification'
    )


@pytest.mark.parametrize('json_data', [
    ({'url': py_url, 'custom_id': '.,/!?'}),
    ({'url': py_url, 'custom_id': 'Hodor-Hodor'}),
    ({'url': py_url, 'custom_id': 'h@k$r'}),
    ({'url': py_url, 'custom_id': '$'}),
    ({'url': py_url, 'custom_id': 'п'}),
    ({'url': py_url, 'custom_id': 'l l'}),
])
def test_invalid_short_url(json_data, client):
    got = client.post('/api/id/', json=json_data)
    assert got.status_code == 400, (
        'If the name for the short link is invalid, the response status should be 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'If the name for the short link is invalid, the key `message` must be in the response'
    )
    assert got.json == {'message': 'Invalid name specified for short link'}, (
        'If the name of the short link is invalid, a message is returned, '
        'not conforming to specification.'
    )
    unique_id = URL_map.query.filter_by(original=py_url).first()
    assert not unique_id, (
        'The short link must allow the use of a strictly defined set '
        'characters. Please refer to the text of the task.'
    )


def test_no_required_field(client):
    try:
        got = client.post('/api/id/', json={
            'short_link': 'python',
        })
    except Exception:
        raise AssertionError(
            'If the body of the request to the `/api/id/` endpoint is different than expected - ',
            'throw an exception.',
        )
    assert got.status_code == 400, (
        'If the body of the request to the `/api/id/` endpoint is different than expected, return '
        'status code 400.'
    )
    assert list(got.json.keys()) == ['message'], (
        'If the body of the request to the `/api/id/` endpoint is different than expected - '
        'return a response with the key `message`.'
    )
    assert got.json == {'message': '\"url\" is a required field!'}, (
        'Message in response body for invalid request body '
        'does not match specification'
    )


def test_url_already_exists(client, short_python_url):
    try:
        got = client.post('/api/id/', json={
            'url': py_url,
            'custom_id': 'py',
        })
    except Exception:
        raise AssertionError(
            'When trying to create a link with a short name that is already taken - ',
            'raise an exception.',
        )
    assert got.status_code == 400, (
        'When trying to create a link with a short name that is already taken - '
        'return status code 400'
    )
    assert list(got.json.keys()) == ['message'], (
        'When trying to create a link with a short name that is already taken - '
        'return a response with the key `message`.'
    )
    assert got.json == {'message': 'The name "py" is already taken.'}, (
        'Trying to create a link with a short name that is already taken '
        'a message is returned with text that does not match the specification.'
    )


@pytest.mark.parametrize('json_data', [
    ({'url': py_url, 'custom_id': None}),
    ({'url': py_url, 'custom_id': ''}),
])
def test_generated_unique_short_id(json_data, client):
    try:
        got = client.post('/api/id/', json=json_data)
    except Exception:
        raise AssertionError(
            'For a request where short_id is missing or empty '
            'string - generate a unique short_id.'
        )
    assert got.status_code == 201, (
        'When creating a short link without an explicit name '
        'should return status code 201'
    )
    unique_id = URL_map.query.filter_by(original=py_url).first()
    assert unique_id, (
        'When creating a short link without an explicit name '
        'need to generate the relative part of the link '
        'from numbers and Latin characters - and save the link in the database'
    )
    assert got.json == {
        'url': py_url,
        'short_link': 'http://localhost/' + unique_id.short,
    }, (
        'When creating a short link without an explicit name '
        'need to generate the relative part of the link '
        'from digits and Latin characters - and return a link in the API response.'
    )


def test_get_url_endpoint(client, short_python_url):
    got = client.get(f'/api/id/{short_python_url.short}/')
    assert got.status_code == 200, (
        'In response to a GET request to the `/api/id/<short_id>/` endpoint, status code 200 should be returned'
    )
    assert list(got.json.keys()) == ['url'], (
        'The GET request to the `/api/id/<short_id>/` endpoint must contain the key `url`'
    )
    assert got.json == {'url': py_url}, (
        'A GET request to the `/api/id/<short_id>/` endpoint returns a response, '
        'not conforming to specification.'
    )


def test_get_url_not_found(client):
    got = client.get('/api/id/{enexpected}/')
    assert got.status_code == 404, (
        'In response to a GET request for a non-existent link '
        'should return status code 404.'
    )
    assert list(got.json.keys()) == ['message'], (
        'The response to a GET request to get a non-existent link must be '
        'passed key `message`'
    )
    assert got.json == {'message': 'The specified id was not found'}, (
        'A GET request for a non-existent link returns a response, '
        'does not match specification.'
    )


def test_len_short_id_api(client):
    long_string = 'CuriosityisnotasinHarryHoweverfromtimetotimeyoushouldexercisecaution'
    got = client.post('/api/id/', json={
        'url': py_url,
        'custom_id': long_string,
    })
    assert got.status_code == 400, (
        'If POST request to endpoint `/api/id/` '
        'field `short_id` contains a string longer than 16 characters - should return status code 400.'
    )
    assert list(got.json.keys()) == ['message'], (
        'If POST request to endpoint `/api/id/` '
        'the `short_id` field contains a string longer than 16 characters - the response should be '
        'key `message`.'
    )
    assert got.json == {'message': 'Invalid name specified for short link'}, (
        'When making a POST request to the `/api/id/` endpoint, in the `short_id` field of which '
        'string is longer than 16 characters, '
        'returned response not conforming to specification.'
    )


def test_len_short_id_autogenerated_api(client):
    client.post('/api/id/', json={
        'url': py_url,
    })
    unique_id = URL_map.query.filter_by(original=py_url).first()
    assert len(unique_id.short) == 6, (
        'For a POST request without a short link in the body, '
        'short link 6 characters long should be generated.'
    )
