from flask import Flask
from flask_session_captcha import FlaskSessionCaptcha

def test_captcha_later_init_app_ok():
    app = Flask(__file__)
    app.config['CAPTCHA_DEBUG_LOG'] = True
    captcha = FlaskSessionCaptcha()    
    captcha.init_app(app)
    assert captcha.should_debug_log == app.config['CAPTCHA_DEBUG_LOG']
    
def test_captcha_init_ok():
    app = Flask(__file__)
    app.config['CAPTCHA_DEBUG_LOG'] = True
    captcha = FlaskSessionCaptcha(app)        
    assert captcha.should_debug_log == app.config['CAPTCHA_DEBUG_LOG']

def test_captcha_config_set_ok(app, captcha):
    """Test captcha config is ok and flask_session_captcha reads all config properly from app.config"""
    assert app.config.get("CAPTCHA_ENABLE") == captcha.enabled
    assert app.config.get("CAPTCHA_LENGTH") == captcha.length
    assert app.config.get("CAPTCHA_WIDTH") == captcha.width
    assert app.config.get("CAPTCHA_HEIGHT") == captcha.height
    assert app.config.get("CAPTCHA_SESSION_KEY") == captcha.session_key
    assert app.config.get("CAPTCHA_INCLUDE_ALPHABET") == captcha.include_alphabet
    assert app.config.get("CAPTCHA_INCLUDE_NUMERIC") == captcha.include_numeric
    assert app.config.get("CAPTCHA_INCLUDE_PUNCTUATION") == captcha.include_punctuation
    assert app.extensions['flask_session_captcha'] == captcha


def test_captcha_enable(app, client, captcha):
    """testing flask_session_captcha.validate method act properly
     with enable option<True, False>"""
    captcha.enabled = False
    assert captcha.validate(value="what ever") == True

    @app.post("/test-captcha/")
    def test():
        if captcha.validate():
            return "OK"
        else:
            return "NOT OK"

    # captcha enable is false so what ever we pass to validate method
    # it should be return True
    assert b'OK' == client.post("/test-captcha/").get_data()

    captcha.enabled = True
    # captcha enable if True so validate method should be return false
    assert b'OK' != client.post("/test-captcha/").get_data()

    captcha.enabled = False


def test_captcha_render_in_template(captcha, client, bind_base_views):
    """Testing captcha is render in template
    with considering enable option
    """
    captcha.enabled = True  # captcha should render in template

    result = client.get("/test/").get_data()
    assert b"class='captcha_is_ok_in_template'" in result
    captcha.enabled = False

    result = client.get("/test/").get_data()
    assert b"class='captcha_is_ok_in_template'" not in result


def test_captcha_wrong_answer(client, captcha, bind_base_views):
    with client:
        result = client.get("/test/")  # generate a captcha
        answer = captcha.get_answer()
        result = client.post("/test/", data={"captcha": "wrong answer", "submit": "submit"}).get_data()
        assert b"NOT OK" == result


def test_captcha_correct_answer(client, captcha, bind_base_views):
    with client:
        result = client.get("/test/")  # generate a captcha
        answer = captcha.get_answer()
        result = client.post("/test/", data={"captcha": answer, "submit": "submit"}).get_data()
        assert b"OK" == result


def test_captcha_no_answer(client, captcha, bind_base_views):
    with client:
        result = client.get("/test/")  # generate a captcha
        answer = captcha.get_answer()
        result = client.post("/test/", data={"submit": "submit"}).get_data()
        assert b"NOT OK" == result


def test_captcha_length(client, app, captcha, bind_base_views):
    """testing captcha length is same as options"""
    with client:
        for i in range(4, 15):
            captcha.length = i
            result = client.get("/test/")  # generate a captcha
            answer = captcha.get_answer()
            assert len(answer) == captcha.length
