# build in
import base64
import secrets
import string
from random import SystemRandom

# lib
from captcha.image import ImageCaptcha
from flask import session, request, Flask, current_app
from markupsafe import Markup


class BaseConfig:
    """ Default configs """
    enabled: bool = True
    should_debug_log: bool = False
    length: int = 4  # minimum length
    session_key: str = "captcha_answer"
    image_generator: ImageCaptcha = None

    width: int = 180,
    height: int = 80,

    _alphabet: str = string.ascii_lowercase
    _punctuation: str = string.punctuation
    _numbers: str = string.digits

    include_alphabet: bool = False
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
        if app is not None:
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
        self.should_debug_log = app.config.get("CAPTCHA_DEBUG_LOG", self.should_debug_log)

        @app.context_processor
        def app_context_processor():
            return {"captcha": self.generate}

        app.extensions['flask_session_captcha'] = self  # bind captcha object to app

    def generate(self, *args, **kwargs) -> Markup:
        """Generate Captcha Image"""
        if not self.enabled:
            return Markup(" ")

        # if none of options passed by developer set all options to False
        answer = self.__generate(include_alphabet=kwargs.get("include_alphabet", self.include_alphabet),
                                         include_punctuation=kwargs.get("include_punctuation", self.include_punctuation),
                                         include_numeric=kwargs.get("include_numeric", self.include_numeric))
        image_data = self.image_generator.generate(answer)
        base64_captcha = base64.b64encode(image_data.getvalue()).decode("ascii")
        self.set_in_session(key=self.session_key, value=answer)
        self.debug_log(f"Captcha Generated. key: {answer}")

        data = f"data:image/png;base64, {base64_captcha}"
        css = f"class=\'{kwargs.get('css_class')}\'" if kwargs.get('css_class', None) else ''
        return Markup(f"<img src='{data}' {css} >")

    def __generate(self, include_alphabet: bool, include_punctuation: bool, include_numeric: bool) -> str:
        """
        generate captcha with given flags
        Don't call this method Directly. use self.generate() instead

            :param:
                include_numeric: if True generate captcha with numeric
                include_alphabet: if True generate captcha with alphabet
                include_punctuation if True generate captcha with punctuation symbols

            :returns:str:
                string value of captcha encoded in base64

       this method generate captcha with default options:
                Baseconfig.include_alphabet: bool = True
                Baseconfig.include_numeric: bool = True
                Baseconfig.include_punctuation: bool = False


        if you want to generate a single captcha with different option you can change it with passing these arguments to
        template filter

        example:
            {{  captcha() }} # generate a captcha with default config or options that sets in app.config
            {{  captcha(include_numeric=True) }} # generate a captcha with only #numeric
            {{  captcha(include_alphabet=True) }} # generate a captcha with only #alphabet

        """
        
        selected = []
                
        if include_punctuation:
            selected.append(self.random_punctuation)
        if include_numeric:
            selected.append(self.random_number)
        if include_alphabet:
            selected.append(self.random_alphabet)

        if len(selected) == 0:
            raise RuntimeError("all options are set to False, <include_numeric, include_alphabet, include_punctuation>. please configure at least one of the options to True")
        
        if self.length <= 0:
            raise ValueError("captcha length should be greater than 0")

        each_option_char_len = self.length // len(selected)

        # calculate evenly space for each option base on options
        answer = []
        for func in selected:
            answer += func(each_option_char_len)

        answer += selected[-1](
            length=(self.length - len(answer)))  # pad the gap with the last option in case of uneven length        
        
        self.shuffle_list(answer)
        answer = "".join(answer)
        return answer        

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
        if self.should_debug_log:
            current_app.logger.debug(message)
