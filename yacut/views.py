import random
import string

from flask import abort, flash, redirect, render_template

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
        if URL_map.query.filter_by(short=short).first() is not None:
            flash(f'Имя {short} уже занято!', 'flash-text')
            return render_template('main.html', form=form)
        if not short:
            short = random_link()
        url = URL_map(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        context = {'form': form, 'short': short}
        flash('Ваша новая ссылка готова:', 'flash-text')
        flash(short, 'flash-link')
        return render_template('main.html', **context)
    return render_template('main.html', form=form)


@app.route('/<string:short>')
def redirect_url(short):
    url = URL_map.query.filter_by(short=short).first()
    if url is None:
        abort(404)
    return redirect(url.original)
