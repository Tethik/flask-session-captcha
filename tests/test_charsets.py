from flask import session, request, Flask, current_app
import string

def test_captcha_mixed_chars(app, client, captcha, bind_base_views):
    """Test captcha with mixed characters. ensure equal distribution of characters"""
    captcha.include_alphabet = True
    captcha.include_numeric = True
    captcha.include_punctuation = True
    captcha.length = 9

    with client:
        client.get("/test/").get_data()
        captcha.generate()
        ans = captcha.get_answer()

        assert len(ans) == captcha.length
        assert sum(1 for char in ans if char.isdigit()) == captcha.length // 3
        assert sum(1 for char in ans if char.isalpha()) == captcha.length // 3
        assert sum(1 for char in ans if char in string.punctuation) == captcha.length // 3
        

def test_captcha_alpha_only(app, client, captcha, bind_base_views):
    """Test captcha with only alphabet characters"""
    captcha.include_alphabet = True
    captcha.include_numeric = False
    captcha.include_punctuation = False
    captcha.length = 9

    with client:
        client.get("/test/").get_data()
        captcha.generate()
        ans = captcha.get_answer()

        assert len(ans) == captcha.length
        assert sum(1 for char in ans if char.isdigit()) == 0
        assert sum(1 for char in ans if char.isalpha()) == captcha.length
        assert sum(1 for char in ans if char in string.punctuation) == 0


def test_captcha_numeric_only(app, client, captcha, bind_base_views):
    """Test captcha with only numeric characters"""
    captcha.include_alphabet = False
    captcha.include_numeric = True
    captcha.include_punctuation = False
    captcha.length = 9

    with client:
        client.get("/test/").get_data()
        captcha.generate()
        ans = captcha.get_answer()

        assert len(ans) == captcha.length
        assert sum(1 for char in ans if char.isdigit()) == captcha.length
        assert sum(1 for char in ans if char.isalpha()) == 0
        assert sum(1 for char in ans if char in string.punctuation) == 0



def test_template_include_alphabet(app, client, captcha, bind_base_views):
    """Test template filter include_alphabet overloads correctly"""
    captcha.include_alphabet = False
    captcha.include_numeric = True
    captcha.include_punctuation = False
    captcha.length = 8

    with client:
        client.get("/test/").get_data()
        captcha.generate(include_alphabet=True)
        ans = captcha.get_answer()

        assert len(ans) == captcha.length
        assert sum(1 for char in ans if char.isdigit()) == captcha.length // 2, "should have half digits"
        assert sum(1 for char in ans if char.isalpha()) == captcha.length // 2, "should have half alphabet"
        assert sum(1 for char in ans if char in string.punctuation) == 0


def test_template_include_numeric(app, client, captcha, bind_base_views):
    """Test template filter include_numeric overloads correctly"""
    captcha.include_alphabet = True
    captcha.include_numeric = False
    captcha.include_punctuation = False
    captcha.length = 8

    with client:
        client.get("/test/").get_data()
        captcha.generate(include_numeric=True)
        ans = captcha.get_answer()

        assert len(ans) == captcha.length
        assert sum(1 for char in ans if char.isdigit()) == captcha.length // 2, "should have half digits"
        assert sum(1 for char in ans if char.isalpha()) == captcha.length // 2, "should have half alphabet"
        assert sum(1 for char in ans if char in string.punctuation) == 0