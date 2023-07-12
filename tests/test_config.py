import os


def test_env_vars():
    assert 'sqlite:///db.sqlite3' in list(os.environ.values()), (
        'Check for the presence of an environment variable with settings for the connection'
        'databases with value sqlite:///db.sqlite3'
    )


def test_config(default_app):
    assert default_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///db.sqlite3', (
        'Check that the config key is SQLALCHEMY_DATABASE_URI '
        'assigned value with settings for database connection'
    )
    assert default_app.config['SECRET_KEY'] == os.getenv('SECRET_KEY'), (
        'Check that the config key is SECRET_KEY '
        'value assigned')
