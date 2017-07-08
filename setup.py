from distutils.command.install_data import install_data

from setuptools import setup, find_packages

VERSION = "0.0.1"
with open("LICENSE") as f:
    LICENSE = f.read()
with open("README.md") as f:
    README = f.read()

setup(
        name='flask_session_captcha',
        version=VERSION,
        author='Joakim Uddholm',
        author_email='tethik@gmail.com',
        description='Simple numeric captcha implementation for flask and flask-session.',
        long_description=README,
        url='https://github.com/Tethik/another-flask-captcha',
        packages=['flask_session_captcha'],
        package_data={'': ['LICENSE', 'README.md']},
        install_requires=[
            'captcha',
            'flask-session',
            'flask'
        ],
        tests_require=[
            'pytest',
            'pytest-cov',
        ],
        license=LICENSE
)