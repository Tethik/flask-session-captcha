import uuid

import redis
from flask import Flask, request, render_template
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha

app = Flask(__name__)


# app config
app.config["SECRET_KEY"] = uuid.uuid4().hex

# captcha config
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 6
app.config["CAPTCHA_WIDTH"] = 200
app.config["CAPTCHA_HEIGHT"] = 160
app.config['CAPTCHA_LETTERS'] = True # include letters
app.config['CAPTCHA_ALPHABET'] = True # include alphabet chart
app.config['CAPTCHA_PUNCTUATION'] = False # include symbols


# session config
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
