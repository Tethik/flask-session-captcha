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


A captcha implemention for flask using `flask-sessionstore <https://pypi.python.org/pypi/Flask-Sessionstore/>`__ and `captcha <https://pypi.python.org/pypi/captcha/>`__ packages. Each captcha challenge answer is saved in the server side session of the challenged client.

For now it supports only simple numeric image captchas, but more could easily be added from the underlying `captcha package <https://pypi.python.org/pypi/captcha/>`__.

Requirements
------------
* `Flask <https://pypi.python.org/pypi/Flask/>`__
* `flask-sessionstore <https://pypi.python.org/pypi/Flask-Sessionstore/>`__ with packages depending on which SESSION_TYPE you use. E.g. sqlalchemy requires flask-sqlalchemy.
* `captcha <https://pypi.python.org/pypi/captcha/>`__

Usage
-----
.. code-block:: python

    import uuid
    import logging
    from flask import Flask, request, render_template
    from flask_sessionstore import Session
    from flask_session_captcha import FlaskSessionCaptcha

    app = Flask(__name__)
    app.config["SECRET_KEY"] = uuid.uuid4()
    app.config['CAPTCHA_ENABLE'] = True
    app.config['CAPTCHA_LENGTH'] = 5
    app.config['CAPTCHA_WIDTH'] = 160
    app.config['CAPTCHA_HEIGHT'] = 60
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    # In case you want to use another key in your session to store the captcha:
    app.config['CAPTCHA_SESSION_KEY'] = 'captcha_image'
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
