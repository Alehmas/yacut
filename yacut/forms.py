from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from settings import MAX_LEN_URL, MIN_LEN_URL


class URLForm(FlaskForm):
    """Form for creating a short link."""

    original_link = URLField(
        'Long link',
        validators=[DataRequired(message='Required field')]
    )
    custom_id = URLField(
        'Your short link',
        validators=[Length(MIN_LEN_URL, MAX_LEN_URL), Optional()]
    )
    submit = SubmitField('Create')
