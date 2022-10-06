import random
import string

from settings import LEN_AUTO_NAME
from .models import URL_map

letters_and_digits = string.ascii_letters + string.digits


def random_link():
    short = ''.join(
        random.choice(letters_and_digits) for i in range(LEN_AUTO_NAME))
    if URL_map.query.filter_by(short=short).first():
        random_link()
    return short
