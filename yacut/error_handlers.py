from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    """Exception class for API error handling."""

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Serialization of the passed error message."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Handling custom exception for API."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Handling the 404 exception."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handling the 500 exception."""
    db.session.rollback()
    return render_template('500.html'), 500
