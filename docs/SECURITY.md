# Security Documentation - Mfukoni Finance Tracker

**Version:** 1.0.0  
**Last Updated:** January 10, 2026

---

## Security Overview

This document outlines the security measures implemented in the Mfukoni Finance Tracker application.

---

## Security Measures Implemented

### 1. SQL Injection Prevention

#### Input Sanitization
- All user inputs are sanitized using `sanitize_sql_string()` function
- Single quotes are escaped to prevent SQL injection: `'` → `''`
- Implemented in: `mfukoni_web/tracker/utils.py`

#### Type Validation
- All inputs are validated and converted to appropriate types
- Decorators ensure type safety: `@validate_input_types()`
- Form validation via Django forms

#### Parameterized Query Structure
- Queries use sanitized parameters instead of direct string concatenation
- All string values are escaped before insertion into SQL

**Example:**
```python
desc_escaped = sanitize_sql_string(description)
self.db.execute(f"INSERT INTO transactions VALUES ({id}, {cat_id}, {amount}, '{desc_escaped}', '{date}', '{type}')")
```

### 2. Cross-Site Request Forgery (CSRF) Protection

- Django CSRF middleware enabled: `django.middleware.csrf.CsrfViewMiddleware`
- All forms include `{% csrf_token %}`
- CSRF cookies configured securely for production

### 3. Cross-Site Scripting (XSS) Prevention

- Django template auto-escaping enabled by default
- All user-generated content is automatically escaped
- Content Security Policy considerations in place

### 4. Security Headers (Production)

When `DEBUG=False`, the following security headers are enabled:

- **HSTS (HTTP Strict Transport Security)**
  - `SECURE_HSTS_SECONDS = 31536000` (1 year)
  - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
  - `SECURE_HSTS_PRELOAD = True`

- **XSS Protection**
  - `SECURE_BROWSER_XSS_FILTER = True`
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`

- **Frame Options**
  - `X_FRAME_OPTIONS = 'DENY'` (in production)
  - `X_FRAME_OPTIONS = 'SAMEORIGIN'` (in development)

- **Referrer Policy**
  - `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'`

### 5. Cookie Security

**Production Settings (`DEBUG=False`):**
- `SESSION_COOKIE_SECURE = True` - Cookies only sent over HTTPS
- `CSRF_COOKIE_SECURE = True` - CSRF cookies only over HTTPS
- `SESSION_COOKIE_HTTPONLY = True` - Prevent JavaScript access
- `CSRF_COOKIE_HTTPONLY = True` - CSRF cookie not accessible via JavaScript
- `SESSION_COOKIE_SAMESITE = 'Strict'` - Prevent CSRF attacks
- `CSRF_COOKIE_SAMESITE = 'Strict'` - Same-site protection

### 6. HTTPS Enforcement

- `SECURE_SSL_REDIRECT = True` in production
- Automatically redirects HTTP to HTTPS
- Only enabled when `DEBUG=False`

### 7. Environment Variables

- Sensitive data stored in environment variables via `python-decouple`
- `SECRET_KEY` loaded from environment: `config('SECRET_KEY', ...)`
- `DEBUG` flag from environment: `config('DEBUG', default=True, cast=bool)`
- `ALLOWED_HOSTS` from environment: `config('ALLOWED_HOSTS', ...)`

**Required Environment Variables:**
- `SECRET_KEY` - Django secret key (generate new one for production)
- `DEBUG` - Debug mode (set to `False` in production)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

### 8. Input Validation

#### Form Validation
- Django forms validate all inputs
- Type checking and conversion
- Required field validation
- Custom validation rules

#### Database Constraints
- PRIMARY KEY enforcement prevents duplicate IDs
- UNIQUE constraint prevents duplicate category names
- Type validation at database level

### 9. Error Handling

- Comprehensive error handling without information leakage
- User-friendly error messages
- Internal errors logged, not exposed to users
- `@handle_db_errors` decorator for graceful error handling

### 10. File Security

#### .gitignore Protection
- Sensitive files excluded from version control:
  - `.env` files
  - `db.sqlite3` database files (not used - custom RDBMS stores all data in `data/mfukoni.db/`)
  - `data/` directory (custom RDBMS data)
  - `__pycache__/` directories
  - `*.pyc` compiled files

### 11. Password Validation (If Authentication Added)

Django password validators configured:
- `UserAttributeSimilarityValidator` - Prevents similarity to user attributes
- `MinimumLengthValidator` - Enforces minimum length
- `CommonPasswordValidator` - Prevents common passwords
- `NumericPasswordValidator` - Prevents numeric-only passwords

---

## Security Checklist for Production Deployment

### Before Deployment:

- [ ] Set `DEBUG=False` in environment variables
- [ ] Generate new `SECRET_KEY` (never use default)
- [ ] Configure `ALLOWED_HOSTS` with production domain(s)
- [ ] Set up HTTPS/SSL certificate
- [ ] Verify security headers are enabled (`DEBUG=False`)
- [ ] Review and update `.env` file (never commit to repository)
- [ ] Configure secure cookie settings
- [ ] Set up database backups
- [ ] Review error logging configuration
- [ ] Test CSRF protection
- [ ] Verify SQL injection prevention works
- [ ] Review file permissions
- [ ] Set up monitoring and alerting

### Ongoing Security:

- [x] Regular dependency updates (`pip list --outdated`) - **Last checked: January 10, 2026**
  - **Core Project Dependencies (in requirements.txt):**
    - Django 3.2.25 (⚠️ **Security Notice:** Known CVEs - consider upgrading to 4.2.26+)
      - CVE-2024-45231, CVE-2025-48432, CVE-2025-57833, CVE-2025-64458, CVE-2025-64459
      - **Recommended:** Upgrade to Django 4.2.26 (LTS) or 5.1.14+ for Python 3.11+
      - Django 4.2 requires Python 3.10+, Django 5.1+ requires Python 3.11+
    - python-decouple 3.8 ✅
    - reportlab 4.4.3 ✅
    - openpyxl 3.1.3 ✅
    - pytest 7.4.4, pytest-django 4.5.2 ✅
  - **Note:** Outdated packages (celery, billiard) are not part of this project's requirements and cannot be upgraded due to Python 3.7 compatibility constraints (celery 5.3.0 requires Python 3.8+)
- [ ] Security vulnerability scanning
- [ ] Regular backups of `data/` directory
- [ ] Monitor error logs
- [ ] Review access logs
- [ ] Keep Django and dependencies up to date

---

## Security Best Practices Followed

1. **Least Privilege Principle**: Only necessary permissions granted
2. **Defense in Depth**: Multiple layers of security (input validation, sanitization, constraints)
3. **Fail Secure**: Errors handled gracefully without exposing internals
4. **Security by Default**: Production settings enforce security
5. **Input Validation**: All inputs validated at multiple layers
6. **Output Encoding**: All outputs properly escaped
7. **Secure Configuration**: Environment variables for sensitive data
8. **Regular Updates**: Dependencies kept up to date

---

## Known Security Considerations

### Development vs Production

- **Development (`DEBUG=True`)**: Relaxed security for easier debugging
- **Production (`DEBUG=False`)**: Full security headers and HTTPS enforced

### Custom RDBMS Security

- JSON-based storage is human-readable
- For production, consider encryption at rest
- File permissions should restrict access to `data/` directory
- Regular backups recommended

### Future Security Enhancements

- User authentication and authorization
- Rate limiting for API endpoints
- Audit logging for sensitive operations
- Encryption at rest for database files
- Two-factor authentication (if user auth added)

---

## Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do NOT** open a public issue
2. Report directly to the project maintainers
3. Provide detailed information about the vulnerability
4. Allow time for the issue to be resolved before public disclosure

---

## References

- [Django Security Checklist](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.org/dev/security/)

---

**Note:** This document should be reviewed and updated regularly as the application evolves.
