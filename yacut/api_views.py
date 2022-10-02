from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import letters_and_digits, random_link


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    url_item = URL_map()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', 400)
    if 'custom_id' in data:
        short = data['custom_id']
        if short == '' or short is None:
            short = random_link()
        if len(short) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400)
        if URL_map.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage(f'Имя \"{short}\" уже занято.', 400)
        for i in short:
            if i not in letters_and_digits:
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки', 400)
    if 'custom_id' not in data:
        short = random_link()
    url_item.original = data['url']
    url_item.short = short
    db.session.add(url_item)
    db.session.commit()
    return jsonify(url_item.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_link = URL_map.query.filter_by(short=short_id).first()
    if url_link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_link.to_dict()['url']}), 200
