import logging

import flask


def test_captcha_config_set_ok(app):
    """Test captcha config is ok and flask_session_captcha reads all config properly from app.config"""
    assert app.config.get("CAPTCHA_ENABLE") == app.extensions['C'].enabled
    assert app.config.get("CAPTCHA_LENGTH") == app.extensions['C'].length
    assert app.config.get("CAPTCHA_WIDTH") == app.extensions['C'].width
    assert app.config.get("CAPTCHA_HEIGHT") == app.extensions['C'].height
    assert app.config.get("CAPTCHA_SESSION_KEY") == app.extensions['C'].session_key
    assert app.config.get("CAPTCHA_INCLUDE_ALPHABET") == app.extensions['C'].include_alphabet
    assert app.config.get("CAPTCHA_INCLUDE_NUMERIC") == app.extensions['C'].include_numeric
    assert app.config.get("CAPTCHA_INCLUDE_PUNCTUATION") == app.extensions['C'].include_punctuation




def test_captcha_enable( app, client):
    """Test flask_session_captcha.validate method in enable True,False"""
    app.extensions['C'].enabled = False
    assert app.extensions['C'].validate(value="what ever") == True


    @app.post("/test-captcha/")
    def test():
        if app.extensions['C'].validate():
            return "OK"
        else:
            return "NOT OK"

    # captcha enable is false so what ever we pass to validate method
    # it should be return True
    assert b'OK' == client.post("/test-captcha/").get_data()

    app.extensions['C'].enabled = True
    # captcha enable if True so validate method should be return false
    assert b'OK' != client.post("/test-captcha/").get_data()

    app.extensions['C'].enabled = False

def test_captcha_length(app):
    ...

def test_captcha_wrong_answer():
    ...


def test_captcha_correct_answer():
    ...