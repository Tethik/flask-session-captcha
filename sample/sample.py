from flask import Flask, request, render_template
from flask_session import Session
from flask_session_captcha import FlaskSessionCaptcha

app = Flask(__name__)
app.config["SECRET_KEY"] = "9a4f5f6e-4973-40f0-b12f-bb87cefdb27b"
app.config['CAPTCHA_ENABLE'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/swb-app.db'
app.config['SESSION_TYPE'] = 'sqlalchemy'
Session(app)

@app.route('/', methods=['POST','GET'])
def some_route():
    captcha = FlaskSessionCaptcha(app)
    if request.method == "POST":
        if captcha.validate():
            return "success"
        else:
            return "fail"

    captcha_img = captcha.generate()
    return render_template("form.html", captcha_img=captcha_img)

if __name__ == "__main__":
    app.debug = True
    app.run()

