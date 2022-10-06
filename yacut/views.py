from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URL_map
from .utils import random_link


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if URL_map.search_short(short) is not None:
            flash(f'Имя {short} уже занято!', 'flash-text')
            return render_template('main.html', form=form)
        if not short:
            short = random_link()
        url = URL_map(
            original=original,
            short=short
        )
        url.add_db()
        context = {'form': form, 'short': short}
        flash('Ваша новая ссылка готова:', 'flash-text')
        flash(short, 'flash-link')
        return render_template('main.html', **context)
    return render_template('main.html', form=form)


@app.route('/<string:short>')
def redirect_url(short):
    url = URL_map.search_short(short)
    if url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original)
