from datetime import datetime

from flask import request

from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, unique=True, nullable=False)
    short = db.Column(db.String, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=request.url_root + self.short
        )

    @staticmethod
    def search_short(short):
        return URL_map.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short):
        url = URL_map(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url
