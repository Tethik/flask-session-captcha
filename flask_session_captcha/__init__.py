import base64
from random import SystemRandom
import logging

from captcha.image import ImageCaptcha
from flask import session, request, Markup

class FlaskSessionCaptcha(object):

    def __init__(self, app):
        self.app = app
        self.enabled = app.config.get("CAPTCHA_ENABLE", True)
        logging.debug(self.enabled)
        self.digits = app.config.get("CAPTCHA_NUMERIC_DIGITS", 4)
        logging.debug(self.digits)
        self.max = 10**self.digits
        self.image_generator = ImageCaptcha()
        self.rand = SystemRandom()        
        
        def generate():
            if not self.enabled:
                return ""
            base64_captcha = self.generate()
            return Markup("<img src='{}'>".format("data:image/png;base64, {}".format(base64_captcha)))

        self.app.jinja_env.globals['captcha'] = generate
        
        # Check for sessions that do not persist on the server. Issue a warning because they are most likely open to replay attacks.
        # This addon is built upon flask-session.
        session_type = app.config.get('SESSION_TYPE', None)
        if session_type is None or session_type == "null":
            raise RuntimeWarning("Flask-Session is not set to use a server persistent storage type. This likely means that captchas are vulnerable to replay attacks.")

    def generate(self):
        """
        Generates and returns a numeric captcha image in base64 format. 
        Saves the correct answer in `session['captcha_answer']`
        Use later as:

        src = captcha.generate()
        <img src="{{src}}">
        """                
        answer = self.rand.randrange(self.max)
        answer = str(answer).zfill(self.digits)        
        image_data = self.image_generator.generate(answer)
        base64_captcha = base64.b64encode(image_data.getvalue()).decode("ascii")
        logging.debug('Generated captcha with answer: ' + answer)
        session['captcha_answer'] = answer
        return base64_captcha


    def validate(self):
        """
        Validate a captcha answer (taken from request.form) against the answer saved in the session.
        Returns always true if CAPTCHA_ENABLED is set to False. Otherwise return true only if it is the correct answer.
        """
        if not self.enabled:
            return True

        if "captcha" not in request.form or "captcha_answer" not in session or not session['captcha_answer']:
            return False
        session_value = session['captcha_answer']

        # invalidate the answer to stop new tries on the same challenge.
        session['captcha_answer'] = None
        return request.form["captcha"].strip() == session_value

    def get_answer(self):
        """
        Shortcut function that returns the currently saved answer.
        """
        return session['captcha_answer']
