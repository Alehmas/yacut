from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from settings import MAX_LEN_URL, MIN_LEN_URL


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(MIN_LEN_URL, MAX_LEN_URL), Optional()]
    )
    submit = SubmitField('Создать')
