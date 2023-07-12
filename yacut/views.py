from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URL_map
from .utils import random_link


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    """Display the link creation form. Create a short link and save to DB."""
    form = URLForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if URL_map.search_short(short) is not None:
            flash(f'The name {short} is already taken!', 'flash-text')
            return render_template('main.html', form=form)
        if not short:
            short = random_link()
        URL_map.create(original, short)
        context = {'form': form, 'short': short}
        flash('Your new link is ready:', 'flash-text')
        flash(short, 'flash-link')
        return render_template('main.html', **context)
    return render_template('main.html', form=form)


@app.route('/<string:short>')
def redirect_url(short):
    """Forwarding to the original address by short link."""
    url = URL_map.search_short(short)
    if url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original)
