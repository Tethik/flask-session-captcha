import uuid
import logging
from flask import Flask, request, render_template
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

app = Flask(__name__)
app.config["SECRET_KEY"] = uuid.uuid4()
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mypassword@127.0.0.1/test'
app.config['SESSION_TYPE'] = 'sqlalchemy'
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
    app.debug = True
    logging.getLogger().setLevel("DEBUG")
    app.run()
