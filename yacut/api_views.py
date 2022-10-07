import re
from http import HTTPStatus

from flask import jsonify, request

from settings import MAX_LEN_URL
from . import app
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import random_link


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(
            '\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    if 'custom_id' in data:
        short = data['custom_id']
        if short == '' or short is None:
            short = random_link()
        if len(short) > MAX_LEN_URL:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST)
        if URL_map.search_short(short) is not None:
            raise InvalidAPIUsage(
                f'Имя \"{short}\" уже занято.', HTTPStatus.BAD_REQUEST)
        for i in short:
            if re.fullmatch(r'[a-zA-Z0-9]+', i) is None:
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки',
                    HTTPStatus.BAD_REQUEST)
    if 'custom_id' not in data:
        short = random_link()
    url_item = URL_map(original=data['url'], short=short)
    url_item.add_db()
    return jsonify(url_item.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_link = URL_map.search_short(short_id)
    if url_link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_link.to_dict()['url']}), HTTPStatus.OK
