from sqlalchemy import inspect

from yacut.models import URL_map


def test_fields(_app):
    inspector = inspect(URL_map)
    fields = [column.name for column in inspector.columns]
    assert all(field in fields for field in ['id', 'original', 'short', 'timestamp']), (
        'All required fields were not found in the model. '
        'Check the model: it should have id, original, short and timestamp fields.'
    )
