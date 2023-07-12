from datetime import datetime

from flask import request

from . import db


class URL_map(db.Model):
    """Model for working with links."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, unique=True, nullable=False)
    short = db.Column(db.String, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Convert data to dictionary."""
        return dict(
            url=self.original,
            short_link=request.url_root + self.short
        )

    @staticmethod
    def search_short(short):
        """Search for a link in the database."""
        return URL_map.query.filter_by(short=short).first()

    @staticmethod
    def create(original, short):
        """Adding a link to the database."""
        url = URL_map(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url
