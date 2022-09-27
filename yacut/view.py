from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def create_short_url():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URL_map.query.filter_by(custom_id=custom_id).first():
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        opinion = URL_map(
            title=form.title.data, 
            text=form.text.data, 
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)