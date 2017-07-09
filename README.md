# flask-session-captcha
[![Build Status](https://travis-ci.org/Tethik/another-flask-captcha.svg?branch=master)](https://travis-ci.org/Tethik/another-flask-captcha)
[![codecov](https://codecov.io/gh/Tethik/another-flask-captcha/branch/master/graph/badge.svg)](https://codecov.io/gh/Tethik/another-flask-captcha)

A captcha implemention for flask using [flask-session](https://github.com/fengsp/flask-session) and [captcha](https://pypi.python.org/pypi/captcha/0.2.3) packages. Each captcha challenge answer is saved in the server side session of the challenged client.

For now it supports only simple numeric image captchas, but more could easily be added from the underlying [captcha package](https://pypi.python.org/pypi/captcha/0.2.3).

## Requirements
* Flask
* Flask-Session
    * ... and different packages depending on which SESSION_TYPE you use. E.g. sqlalchemy requires flask-sqlalchemy.
* captcha

## Usage
```python
import uuid
import logging
from flask import Flask, request, render_template
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha

app = Flask(__name__)
app.config["SECRET_KEY"] = uuid.uuid4()
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_NUMERIC_DIGITS'] = 5
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
app.config['SESSION_TYPE'] = 'sqlalchemy'
Session(app)
captcha = FlaskSessionCaptcha(app)

@app.route('/', methods=['POST','GET'])
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

```

Template can look as follows. `captcha.validate()` will be default try to validate against a form input with name "captcha".

```html
<form method="POST">
    {{ captcha() }} <!-- This renders an <img> tag with the captcha img. -->
    <input type="text" name="captcha">
    <input type="submit">
</form>
```
