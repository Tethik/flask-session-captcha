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
    log: bool = False
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
        self.log = app.config.get("CAPTCHA_LOG", self.log)

        @app.context_processor
        def app_context_processor():
            return {"captcha": self.generate}

        app.extensions['flask_session_captcha'] = self  # bind captcha object to app

    def generate(self, *args, **kwargs) -> Markup:
        """Generate Captcha Image"""
        if not self.enabled:
            return Markup(" ")

        base64_captcha = self.__generate(*args, **kwargs)
        data = f"data:image/png;base64, {base64_captcha}"
        css = f"class=\'{kwargs.get('css_class')}\'" if kwargs.get('css_class', None) else ''
        return Markup(f"<img src='{data}' {css} >")

    def __generate(self, *args, **kwargs) -> str:
        """
            generate captcha with given flags

            :param:
                numeric: if True generate captcha with numeric only
                alphabet: if True generate captcha with alphabet
                punctuation if True generate captcha with punctuation symbols
        ××××
        Don't call this method Directly. use self.generate() instead
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
        base64_captcha = base64.b64encode(image_data.getvalue()).decode("ascii")
        self.set_in_session(key=self.session_key, value=answer)
        self.debug_log(f"Captcha Generated. key: {answer}")
        return base64_captcha

    def validate(self, form_key: str = "captcha", value: str = None) -> bool:
        """
        Validate a captcha answer (taken from request.form) against the answer saved in the session.
        Returns always true if CAPTCHA_ENABLE is set to False. otherwise return true only if it is the correct answer.

        Args:
            from_key: str: key in post request for captcha that user typed in
            value: str:  captcha answer that user typed in

        """
        if not self.enabled:
            return True

        session_value = session.get(self.session_key, None)
        if not session_value:
            return False

        value = request.form.get(form_key, None) or value
        session.pop(self.session_key)
        return value == session_value

    def get_answer(self):
        """
        Shortcut function that returns the currently saved answer.
        """
        return session.get(self.session_key)

    def set_in_session(self, key: str, value: str):
        """Setting a captcha in user's session if captcha enable is on"""
        if self.enabled:
            key = key or self.session_key
            session[key] = value

    def debug_log(self, message: str):
        """Log message to stdout using flask internal logger"""
        if self.log:
            current_app.logger.debug(message)
