# build in
import base64
import secrets
import string
from random import SystemRandom

# lib
from captcha.image import ImageCaptcha
from flask import session, request, Flask, current_app
from markupsafe import Markup

# flask_session_captcha
from . import exception as ex


class BaseConfig:
    """ Default configs """
    enabled: bool = True
    length: int = 4  # minimum length
    session_key: str = "captcha_answer"
    image_generator: ImageCaptcha = None

    width: int = 180,
    height: int = 80,

    _alphabet: str = string.ascii_lowercase
    _punctuation: str = string.punctuation
    _numbers: str = string.digits

    include_alphabet: bool = True
    include_numeric: bool = True
    include_punctuation: bool = False

    random = SystemRandom()

    def random_number(self, length: int) -> list:
        return [secrets.choice(self._numbers) for i in range(length)]

    def random_punctuation(self, length: int) -> list:
        return [secrets.choice(self._punctuation) for i in range(length)]

    def random_alphabet(self, length: int) -> list:
        return [secrets.choice(self._alphabet) for i in range(length)]

    def shuffle_list(self, list_captcha: list) -> None:
        self.random.shuffle(list_captcha)


class FlaskSessionCaptcha(BaseConfig):

    def __init__(self, app: Flask = None):
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f"object {app} not a Flask instance.")

        self.init_app(app)

    def init_app(self, app: Flask):
        """
        Initialize the captcha extension to the given app object.

        :param app: Flask Object
        """
        self.enabled = app.config.get("CAPTCHA_ENABLE", self.enabled)
        self.length = app.config.get("CAPTCHA_LENGTH", self.length)
        self.width = app.config.get("CAPTCHA_WIDTH", self.width)
        self.height = app.config.get("CAPTCHA_HEIGHT", self.height)
        self.session_key = app.config.get("CAPTCHA_SESSION_KEY", self.session_key)
        self.image_generator = ImageCaptcha(**{'width': self.width, 'height': self.height})
        self.include_alphabet = app.config.get("CAPTCHA_INCLUDE_ALPHABET", self.include_alphabet)
        self.include_numeric = app.config.get("CAPTCHA_INCLUDE_NUMERIC", self.include_numeric)
        self.include_punctuation = app.config.get("CAPTCHA_INCLUDE_PUNCTUATION", self.include_punctuation)

        def _generate(*args, **kwargs) -> Markup:
            """Generate Captcha Image"""
            if not self.enabled:
                return Markup(" ")

            base64_captcha = self.generate(*args, **kwargs)
            data = f"data:image/png;base64, {base64_captcha}"
            css = f"class=\'{kwargs.get('css_class')}\'" if kwargs.get('css_class', None) else ''
            return Markup(f"<img src='{data}' {css} >")

        app.jinja_env.globals['captcha'] = _generate

    def generate(self, *args, **kwargs) -> str:
        """
            generate captcha with given flags

            :param:
                numeric: if True generate captcha with numeric only
                alphabet: if True generate captcha with alphabet
                punctuation if True generate captcha with punctuation symbols

            if both alphabet and numeric set to True this function generate captcha that contain both alphabet and numeric

        """

        if not kwargs.get("numeric"):
            numeric = self.include_numeric
        if not kwargs.get("alphabet"):
            alphabet = self.include_alphabet
        if not kwargs.get("punctuation"):
            punctuation = self.include_punctuation

        # single mode captcha options
        answer = []
        if numeric and not alphabet and not punctuation:
            answer += self.random_number(length=self.length)
        if alphabet and not numeric and not punctuation:
            answer += self.random_alphabet(length=self.length)
        if punctuation and not numeric and not alphabet:
            answer += self.random_punctuation(length=self.length)

        if len(answer) == 0:  # mix captcha mode
            selected = {}
            if punctuation:
                selected["punctuation"] = self.random_punctuation
            if numeric:
                selected["numeric"] = self.random_number
            if alphabet:
                selected["alphabet"] = self.random_alphabet

            total = sum([alphabet, numeric, punctuation])
            each_round = self.length // total
            for each in selected:
                answer += (selected[each](length=each_round))

            answer += (self.random_alphabet(length=(self.length - len(answer))))
            self.shuffle_list(answer)

        answer = "".join(answer)
        image_data = self.image_generator.generate(answer)
        base64_captcha = base64.b64encode(
            image_data.getvalue()).decode("ascii")
        current_app.logger.debug(f'Captcha Generated:\nKey:{answer}\tAnswer:{answer}')
        session[self.session_key] = answer
        return base64_captcha

    def validate(self, form_key: str = "captcha", value: str = None) -> bool:
        """
        Validate a captcha answer (taken from request.form) against the answer saved in the session.
        Returns always true if CAPTCHA_ENABLE is set to False. Otherwise return true only if it is the correct answer.
        """
        if not self.enabled:
            return True

        session_value = session.get(self.session_key, None)
        if not session_value:
            return False

        value = request.form.get(form_key, None)
        session.pop(self.session_key)
        return value == session_value

    def get_answer(self):
        """
        Shortcut function that returns the currently saved answer.
        """
        return session.get(self.session_key)
