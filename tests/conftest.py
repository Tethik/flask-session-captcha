import os
import pytest
from flask import Flask
from flask_session_captcha import FlaskSessionCaptcha
from flask_session import Session

@pytest.fixture()
def app():
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'DEBUG': True,
        'SECRET_KEY': os.urandom(24)
    })

    # captcha configs:
    app.config['CAPTCHA_ENABLE'] = True
    app.config['CAPTCHA_LENGTH'] = 5
    app.config['CAPTCHA_WIDTH'] = 200
    app.config['CAPTCHA_HEIGHT'] = 160
    app.config['CAPTCHA_INCLUDE_NUMERIC'] = True
    app.config['CAPTCHA_INCLUDE_ALPHABET'] = True
    app.config['CAPTCHA_INCLUDE_PUNCTUATION'] = False
    app.config['CAPTCHA_SESSION_KEY'] = 'test_captcha_image'
    # session config
    app.config['SESSION_TYPE'] = 'redis'
    Session(app)

    captcha_object = FlaskSessionCaptcha(app=app)
    app.extensions['C'] = captcha_object

    yield app

@pytest.fixture()
def client(app):
    yield app.test_client()

