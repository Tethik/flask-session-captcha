import os

import pytest
from flask import Flask, render_template
from flask_session import Session

from flask_session_captcha import FlaskSessionCaptcha


@pytest.fixture()
def app():
    """
    Creating Flask Application + adding base config for flask captcha session packages
    """
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'DEBUG': True,
        'SECRET_KEY': os.urandom(24)
    })

    # captcha configs:
    app.config['CAPTCHA_ENABLE'] = True
    app.config['CAPTCHA_LOG'] = False
    app.config['CAPTCHA_LENGTH'] = 4
    app.config['CAPTCHA_WIDTH'] = 200
    app.config['CAPTCHA_HEIGHT'] = 160
    app.config['CAPTCHA_INCLUDE_NUMERIC'] = True
    app.config['CAPTCHA_INCLUDE_ALPHABET'] = True
    app.config['CAPTCHA_INCLUDE_PUNCTUATION'] = False
    app.config['CAPTCHA_SESSION_KEY'] = 'test_captcha_image'

    # session config
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    captcha = FlaskSessionCaptcha(app=app)

    yield app


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def captcha(app):
    yield app.extensions['flask_session_captcha']


@pytest.fixture()
def bind_base_views(app, captcha):
    """adding base views to flask application for testing captcha validate method"""

    @app.get("/test/")
    def index_get():
        return render_template("index.html")

    @app.post("/test/")
    def index_post():
        if captcha.validate():
            return "OK"
        else:
            return "NOT OK"
