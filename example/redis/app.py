import uuid
try:
    import redis
except ImportError:
    raise ImportError("redis package was not installed. install it via `pip install redis` ")

try:
    from flask_session import Session
except ImportError:
    raise ImportError("flask-session package was not installed. install it via `pip install flask-session` ")

from flask import Flask, request, render_template
from flask_session_captcha import FlaskSessionCaptcha

app = Flask(__name__)


# app config
app.config["SECRET_KEY"] = uuid.uuid4().hex

# captcha config
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 6
app.config["CAPTCHA_WIDTH"] = 400
app.config["CAPTCHA_HEIGHT"] = 160
app.config['CAPTCHA_INCLUDE_ALPHABET'] = False # include alphabet<letters>
app.config['CAPTCHA_INCLUDE_NUMERIC'] = True # include numeric
app.config['CAPTCHA_INCLUDE_PUNCTUATION'] = False # include symbols


# flask-session config https://flask-session.readthedocs.io/en/latest/
app.config['SESSION_TYPE'] = 'redis'
app.config["SESSION_REDIS"] = redis.Redis()


Session(app)
captcha = FlaskSessionCaptcha(app)


@app.route('/', methods=['POST', 'GET'])
def some_route():
    if request.method == "POST":
        if captcha.validate():
            return "success"
        else:
            return "fail"

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
