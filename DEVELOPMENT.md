## Testing

```bash
pytest --cov=flask_session_captcha --cov-report=term-missing
```

## Releasing to pypi
```bash
python setup.py bdist_wheel
gpg --detach-sign -a dist/<the newly created wheel>
twine 
```