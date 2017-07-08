# another-flask-captcha
A captcha implemention for flask

## Usage
```python
app = Flask(__name__)
captcha = FlaskSessionCaptcha(app)

@app.route('/')
def some_route():    
    if request.method == "POST":
        if captcha.validate():
            return "success"
        else:
            return "fail"

    captcha_img = captcha.generate()
    return render_template("form.html", captcha_img=captcha_img)

```

In the template:

```html
<form method="POST">
    {{ captcha() }}
    <input type="submit">
</form>
```