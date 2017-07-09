=====================
flask-session-captcha
=====================

.. image:: https://travis-ci.org/Tethik/another-flask-captcha.svg?branch=master
    :target: https://travis-ci.org/Tethik/another-flask-captcha
    :alt: Travis-CI

.. image:: https://codecov.io/gh/Tethik/another-flask-captcha/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Tethik/another-flask-captcha
    :alt: codecov

.. image:: https://img.shields.io/pypi/v/nine.svg   
    :target: https://pypi.python.org/pypi/flask-session-captcha
    :alt: Latest version    

.. image:: https://img.shields.io/pypi/pyversions/flask-session-captcha.svg
    :target: https://pypi.python.org/pypi/flask-session-captcha
    :alt: Supported python versions
    
.. image:: https://img.shields.io/github/license/Tethik/flask-session-captcha.svg   
    :target: https://github.com/Tethik/flask-session-captcha/blob/master/LICENSE


A captcha implemention for flask using `flask-session <https://github.com/fengsp/flask-session>`__ and `captcha <https://pypi.python.org/pypi/captcha/0.2.3>`__ packages. Each captcha challenge answer is saved in the server side session of the challenged client.

For now it supports only simple numeric image captchas, but more could easily be added from the underlying `captcha package <https://pypi.python.org/pypi/captcha/0.2.3>`__.

Requirements
------------
* Flask
* Flask-Session
    * ... and different packages depending on which SESSION_TYPE you use. E.g. sqlalchemy requires flask-sqlalchemy.
* captcha

Usage
-----
.. code-block:: python

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



Template can look as follows. `captcha.validate()` will be default try to validate against a form input with name "captcha".

.. code-block:: html

    <form method="POST">
        {{ captcha() }} <!-- This renders an <img> tag with the captcha img. -->
        <input type="text" name="captcha">
        <input type="submit">
    </form>
