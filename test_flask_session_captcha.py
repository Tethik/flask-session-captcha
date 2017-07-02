import multiprocessing
import logging
import sys

import pytest
import requests
from flask import Flask, session, request
from flask_session_captcha import FlaskSessionCaptcha
from flask_session import Session
from parsel import Selector

@pytest.fixture()
def run_app():
    class zzz:
        p = None

    def function(app, port):
        @app.route('/kill')
        def kill():
            request.environ.get('werkzeug.server.shutdown')()
            return ""

        @app.route('/status')
        def status():
            return "1"

        def run_server():
            print("starting app..")
            app.run(host="127.0.0.1", port=port)

        zzz.p = multiprocessing.Process(target=run_server)
        zzz.p.start()

        #try until we can connect
        while True:
            url = 'http://127.0.0.1:{}/status'.format(port)
            logging.debug("Trying to connect to server: " + url)
            try:
                requests.get(url)
                break
            except:
                pass

    yield function

    if zzz.p:
        zzz.p.terminate()

def _default_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aba'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/swbcommon-test-session.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['CAPTCHA_ENABLED'] = True
    app.config['CAPTCHA_NUMERIC_DIGITS'] = 5
    return app

def _default_routes(captcha, app):
    @app.route("/", methods=["POST","GET"])
    def hello():
        if request.method == "POST":
            if captcha.validate():
                return "ok"
            return "nope"
        captcha.generate()
        return str(captcha.get_answer())

def test_captcha(run_app):    
    app = _default_app()
    captcha = FlaskSessionCaptcha(app)
    _default_routes(captcha, app)
    Session(app)

    run_app(app, 5000)
    logging.basicConfig(stream=sys.stderr, level="INFO")

    # try without any session or csrf value
    r = requests.post("http://localhost:5000/", data={"s": "something"})
    assert r.text == "nope"
    r = requests.post("http://localhost:5000/", data={"s": "something", "captcha": ""})
    assert r.text == "nope"
    r = requests.post("http://localhost:5000/", data={"s": "something", "captcha": "also wrong"})
    assert r.text == "nope"

    # without right cookie
    r = requests.get("http://localhost:5000/")
    r = requests.post("http://localhost:5000/", data={"s": "something", "captcha": r.text})
    assert r.text == "nope" # no session

    # everything ok
    s = requests.Session()
    r = s.get("http://localhost:5000/")
    r = s.post("http://localhost:5000/", data={"s": "something", "captcha": r.text})
    assert r.text == "ok"

    # wrong number
    s = requests.Session()
    r = s.get("http://localhost:5000/")
    r = s.post("http://localhost:5000/", data={"s": "something", "captcha": "wrong"})
    assert r.text == "nope"

def test_captcha_replay(run_app):
    app = _default_app()
    captcha = FlaskSessionCaptcha(app)
    _default_routes(captcha, app)
    Session(app)

    run_app(app, 5000)
    logging.basicConfig(stream=sys.stderr, level="INFO")

    # everything ok    
    r = requests.get("http://localhost:5000/")
    captcha_value = r.text
    cookies = r.cookies
    r = requests.post("http://localhost:5000/", cookies=cookies, data={"s": "something", "captcha": captcha_value})
    assert r.text == "ok"
    r = requests.post("http://localhost:5000/", cookies=cookies, data={"s": "something", "captcha": captcha_value})
    assert r.text == "nope"

def test_captcha_passthrough_when_disabled(run_app):
    app = _default_app()
    app.config["CAPTCHA_ENABLED"] = False
    captcha = FlaskSessionCaptcha(app)
    _default_routes(captcha, app)
    Session(app)

    run_app(app, 5000)
    logging.basicConfig(stream=sys.stderr, level="INFO")

    # everything ok    
    r = requests.get("http://localhost:5000/")
    captcha_value = r.text
    cookies = r.cookies
    r = requests.post("http://localhost:5000/", cookies=cookies, data={"s": "something", "captcha": captcha_value})
    assert r.text == "ok"
    r = requests.get("http://localhost:5000/")

    captcha_value = "false"
    cookies = r.cookies
    r = requests.post("http://localhost:5000/", cookies=cookies, data={"s": "something", "captcha": captcha_value})
    assert r.text == "ok"

def test_captcha_least_digits(run_app):
    app = _default_app()
    app.config["CAPTCHA_NUMERIC_DIGITS"] = 8
    captcha = FlaskSessionCaptcha(app)
    _default_routes(captcha, app)
    Session(app)

    run_app(app, 5000)
    logging.basicConfig(stream=sys.stderr, level="INFO")

    # everything ok    
    r = requests.get("http://localhost:5000/")
    captcha_value = r.text
    assert len(captcha_value) == 8

# def test_without_server(run_app):
#     app = _default_app()
#     app.config["CAPTCHA_NUMERIC_DIGITS"] = 8
#     captcha = FlaskSessionCaptcha(app)
#     run_app(app, 5000)

#     captcha.generate()
#     answer = captcha.get_answer()
#     assert answer < 10**8
#     assert not captcha.validate()
#     session["captcha_answer"] = 2
#     assert not captcha.validate()
#     session["captcha_answer"] = answer
#     assert captcha.validate()
    
    