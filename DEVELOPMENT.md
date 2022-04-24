## Testing

```bash
pytest --cov=flask_session_captcha --cov-report=term-missing
```

## Releasing to pypi
1. Bump `VERSION` in setup.py
2. Git tag `v` + VERSION
3. Create release on github
4. Github action handles the rest :)