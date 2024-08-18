
# flask-session-captcha

[![Latest version](https://img.shields.io/pypi/v/flask-session-captcha.svg)](https://pypi.python.org/pypi/flask-session-captcha)
[![Supported python versions](https://img.shields.io/pypi/pyversions/flask-session-captcha.svg)](https://pypi.python.org/pypi/flask-session-captcha)
[![License](https://img.shields.io/github/license/Tethik/flask-session-captcha.svg)](https://github.com/Tethik/flask-session-captcha/blob/master/LICENSE)

[![Downloads](https://static.pepy.tech/badge/flask-session-captcha)](https://pepy.tech/project/flask-session-captcha)
[![Downloads](https://static.pepy.tech/badge/flask-session-captcha/month)](https://pepy.tech/project/flask-session-captcha)
[![Downloads](https://static.pepy.tech/badge/flask-session-captcha/week)](https://pepy.tech/project/flask-session-captcha)

****
A captcha implemention for flask using [flask-session](https://pypi.python.org/pypi/Flask-Session/) and [captcha](https://pypi.python.org/pypi/captcha/) packages. 
Each captcha challenge answer is saved in the server side session of the challenged client.
Support for different types of captchas such as numeric/letter/symbol captchas.

## Requirements
* [Flask](https://pypi.python.org/pypi/Flask/)
* [flask-session](https://pypi.python.org/pypi/Flask-Session/) with packages depending on which SESSION_TYPE you use. E.g. sqlalchemy requires flask-sqlalchemy.
* [captcha](https://pypi.python.org/pypi/captcha/)

## Changelog

* **1.4.2** - Bump pillow from 10.2.0 to 10.3.0 by @dependabot in #49
* **1.4.1** - Fix error thrown when flask-session-captcha is init-ed without a Flask app object. Rename CAPTCHA_LOG environment variable to CAPTCHA_DEBUG_LOG.
* **1.4.0** - Migrated from `flask-sessionstore` to `flask-session`. Added functionality for alphabetic and punctuation characters to be included in the captcha (thanks @alisharify7). Support moved to python 3.8, 3.9, 3.10, 3.11.

## Usage
```python
import uuid
import logging
from flask import Flask, request, render_template
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha

app = Flask(__name__)
app.config["SECRET_KEY"] = uuid.uuid4().hex

# captcha configs:
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['CAPTCHA_WIDTH'] = 200
app.config['CAPTCHA_HEIGHT'] = 160
# app.config['CAPTCHA_LOG'] = False # log information to terminal
# app.config['CAPTCHA_INCLUDE_ALPHABET'] = False
# app.config['CAPTCHA_INCLUDE_NUMERIC'] = True
# app.config['CAPTCHA_INCLUDE_PUNCTUATION'] = False
# app.config['CAPTCHA_SESSION_KEY'] = 'captcha_image' # In case you want to use another key in your session to store the captcha

# session config
app.config['SESSION_TYPE'] = 'redis' # or other type of drivers for session, see https://flask-session.readthedocs.io/en/latest/
Session(app)
captcha = FlaskSessionCaptcha(app)

@app.route('/', methods=['POST','GET'])
def some_route():
    if request.method == "POST":
        if captcha.validate():
            return "captcha validated successfully"
        else:
            return "invalid captcha/answer"

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
```


Template can look as follows. `captcha.validate()` will be default try to validate against a form input with name "captcha".

```html
<form method="POST">
    {{ captcha() }} <!-- This renders an <img> tag with the captcha img. -->
    <input type="text" name="captcha">
    <input type="submit">
</form>
```

It can also take a `css_class` argument to add classes to the generated DOM:

```html
<form method="POST">
    {{ captcha(css_class="captcha") }}
    <input type="text" name="captcha">
    <input type="submit">
</form>
```

You can also override settings for the captcha contents itself, via `include_alphabet`, `include_numeric` and `include_punctuation`.
Like so:

```html
<form method="POST">
    {{ captcha(include_alphabet=True) }}
    <input type="text" name="captcha">
    <input type="submit">
</form>
```
