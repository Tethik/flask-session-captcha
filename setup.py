from setuptools import setup

VERSION = "1.5.0"
with open("README.md") as f:
    README = f.read()

setup(
    name='flask_session_captcha',
    version=VERSION,
    author='Joakim Uddholm',
    author_email='tethik@gmail.com',
    description='Captcha implementation for flask and flask-session.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Tethik/flask-session-captcha',
    packages=['flask_session_captcha'],
    package_data={'': ['LICENSE', 'README.md']},
    install_requires=[
        'captcha',
        'Flask',
        'markupsafe',
    ],
    tests_require=[
        'flake8',
        'flask_session',
        'cachelib',
        'pytest',
        'pytest-cov',
        'redis'
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Security',
    ],
    license='MIT'
)
