# Security Review: HTTPS and Secure Headers

## Settings Configured in settings.py

- SECURE_SSL_REDIRECT: Redirects HTTP to HTTPS.
- SECURE_HSTS_SECONDS: Instructs browsers to only use HTTPS for 1 year.
- ...
(continue for each setting with explanation)

## Web Server Configuration

Configured nginx with SSL certificate to serve app over HTTPS.

## Potential Areas of Improvement

- Add CSP headers for content security policy.
- Regularly rotate SSL certificates.
