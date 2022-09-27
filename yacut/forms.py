from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте длинную ссылку',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Добавьте для короткую ссылку',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')