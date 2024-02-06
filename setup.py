from setuptools import setup

VERSION = "1.4.0"
with open("README.rst") as f:
    README = f.read()

setup(
    name='flask_session_captcha',
    version=VERSION,
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Captcha implementation for flask and flask-session.',
    long_description=README,
    url='https://github.com/Tethik/flask-session-captcha',
    packages=['flask_session_captcha'],
    package_data={'': ['LICENSE', 'README.rst']},
    install_requires=[
        'captcha',
        'Flask',
        'markupsafe',
    ],
    tests_require=[
        'flake8',
        'pytest',
        'pytest-cov',
        'Flask-SQLAlchemy',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security',
    ],
    license='MIT'
)
