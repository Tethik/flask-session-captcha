=====================
flask-session-captcha
=====================

.. image:: https://img.shields.io/pypi/v/flask-session-captcha.svg   
    :target: https://pypi.python.org/pypi/flask-session-captcha
    :alt: Latest version    

.. image:: https://img.shields.io/pypi/pyversions/flask-session-captcha.svg
    :target: https://pypi.python.org/pypi/flask-session-captcha
    :alt: Supported python versions
    
.. image:: https://img.shields.io/github/license/Tethik/flask-session-captcha.svg   
    :target: https://github.com/Tethik/flask-session-captcha/blob/master/LICENSE


A captcha implemention for flask using `flask-session <https://pypi.python.org/pypi/Flask-Session/>`__ and `captcha <https://pypi.python.org/pypi/captcha/>`__ packages. Each captcha challenge answer is saved in the server side session of the challenged client.
Support for different types of captchas such as
   Numeric/letter/symbol captchas

Requirements
------------
* `Flask <https://pypi.python.org/pypi/Flask/>`__
* `flask-session <https://pypi.python.org/pypi/Flask-Session/>`__ with packages depending on which SESSION_TYPE you use. E.g. sqlalchemy requires flask-sqlalchemy.
* `captcha <https://pypi.python.org/pypi/captcha/>`__

Usage
-----
.. code-block:: python

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
    app.config['CAPTCHA_INCLUDE_ALPHABET'] = True
    app.config['CAPTCHA_INCLUDE_NUMERIC'] = True
    app.config['CAPTCHA_INCLUDE_PUNCTUATION'] = False
    app.config['CAPTCHA_SESSION_KEY'] = 'captcha_image' # In case you want to use another key in your session to store the captcha:

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



Template can look as follows. `captcha.validate()` will be default try to validate against a form input with name "captcha".

.. code-block:: html

    <form method="POST">
        {{ captcha() }} <!-- This renders an <img> tag with the captcha img. -->
        <input type="text" name="captcha">
        <input type="submit">
    </form>

It can also take a `css_class` argument to add classes to the generated DOM:

.. code-block:: html

    <form method="POST">
        {{ captcha(css_class="captcha") }}
        <input type="text" name="captcha">
        <input type="submit">
    </form>
