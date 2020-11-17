# Flask-session-captcha MongoDB Sample

You can learn Flask Session captcha store in MongoDB with this sample.

# Quick Introduction
Flask-session-captcha creates captcha image.

```     {{ captcha() }}  ```

It stores the captcha code in **flask_sessionstore** database inside **sessions** collection as document.

You can read more over [here](https://flask-session.readthedocs.io/en/latest/)

## Install

Install the required dependencies:

    $ pip install -U Flask flask-session-captcha Flask-Sessionstore pymongo

## Run

Start server with:

python sample.py

Then visit:

    http://127.0.0.1:5000/
