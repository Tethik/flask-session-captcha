## Testing

```bash
pytest --cov=flask_session_captcha --cov-report=term-missing
```

## Releasing to pypi
1. Bump `VERSION` in setup.py
2. Git tag `v` + VERSION
3. Create release on github
4. Github action handles the rest :)




## TODO
1. adding new method for logging data in terminal base on CAPTCHA_LOG env
2. adding new test for testing template rendering with all options <include_alphabet, include_numeric, include_punctuation>
3. 