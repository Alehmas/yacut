# from random import randrange
import string
import random

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URL_map


letters_and_digits = string.ascii_letters + string.digits

def random_link():
    short = ''.join(random.choice(letters_and_digits) for i in range(6))
    if URL_map.query.filter_by(short=short).first():
        random_link()
    return short

@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if URL_map.query.filter_by(original=original).first():
            flash('Для этой ссылки уже есть корткая ссылка')
            return render_template('main.html', form=form)
        if URL_map.query.filter_by(short=short).first():
            flash('Этот вариант коротнкой ссылки уже занят')
            return render_template('main.html', form=form)
        if not short:
            short = random_link()
        url = URL_map(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return redirect(url_for('main.html', id=url.id))
    return render_template('main.html', form=form)


# redirect_url