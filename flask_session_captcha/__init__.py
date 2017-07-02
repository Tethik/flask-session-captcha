import base64
from random import SystemRandom
import logging

from captcha.image import ImageCaptcha
from flask import session, g, request

rand = SystemRandom()
image = ImageCaptcha()

class FlaskSessionCaptcha(object):

    def __init__(self, app):
        self.app = app
        self.enabled = app.config.get("CAPTCHA_ENABLED", True)
        self.digits = app.config.get("CAPTCHA_NUMERIC_DIGITS", 4)
        self.max = 10**self.digits
        
        # TODO check for sessions that do not persist on the server. 
        # E.g. sessions saved in the cookie.
        # Issue a warning because they are most likely open to replay attacks.

    def generate(self):
        """
        Generates and returns a numeric captcha image in base64 format. 
        Saves the correct answer in `session['captcha_answer']`
        Use later as:

        src = captcha.generate()
        <img src="{{src}}">
        """   
        answer = rand.randrange(self.max)
        session['captcha_answer'] = str(answer).zfill(self.digits)        
        image_data = image.generate(session['captcha_answer'])
        g.base64_captcha = base64.b64encode(image_data.getvalue()).decode("ascii")
        logging.debug('Generated captcha with answer: ' + session['captcha_answer'])
        return g.base64_captcha

    def validate(self):
        """
        Validate a captcha answer (taken from request.form) against the answer saved in the session.
        Returns always true if CAPTCHA_ENABLED is set to False. Otherwise return true only if it is the correct answer.
        """
        if not self.enabled:
            return True

        if not ("captcha" in request.form and "captcha_answer" in session):
            return False
        if not session['captcha_answer']:
            return False
        session_value = session['captcha_answer']

        # invalidate the answer to stop new tries on the same challenge.
        session['captcha_answer'] = None
        return request.form["captcha"].strip() == session_value

    @staticmethod
    def get_answer():
        """
        Shortcut function that returns the currently saved answer.
        """
        return session['captcha_answer']
