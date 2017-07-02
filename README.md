# another-flask-captcha
A captcha implemention for flask

## Usage
```python
app = Flask(__name__)

@app.route('/')
def some_route():
    captcha = FlaskSessionCaptcha(app)
    if request.method == "POST":
        if captcha.validate():
            return "success"
        else:
            return "fail"

    captcha_img = captcha.generate()
    return render_template("form.html", captcha_img=captcha_img)

```

```html
<form method="post">
    <img src="{{captcha_img}}">
    <input type="text" name="captcha">
    <input type="submit" name="submit">
</form>
```