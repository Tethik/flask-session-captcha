# flask-session-captcha
[![travis](https://travis-ci.org/Tethik/another-flask-captcha.svg)](https://travis-ci.org/Tethik/another-flask-captcha)
[![codecov](https://codecov.io/gh/Tethik/another-flask-captcha/branch/master/graph/badge.svg)](https://codecov.io/gh/Tethik/another-flask-captcha)

A captcha implemention for flask

## Usage
```python
import uuid
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

@app.route('/')
def some_route():    
    if request.method == "POST":
        if captcha.validate():
            return "success"
        else:
            return "fail"

    return render_template("form.html")
```

Template can look as follows. `captcha.validate()` will be default try to validate against a form input with name "captcha".

```html
<form method="POST">
    {{ captcha() }}
    <input type="text" name="captcha">
    <input type="submit">
</form>
```