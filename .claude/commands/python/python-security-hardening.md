# Python Security Hardening

Implement comprehensive security hardening for Python applications following OWASP guidelines and modern security best practices

## Instructions

Follow this systematic approach to harden Python application security: **$ARGUMENTS**

1. **Security Assessment and Environment Analysis**
   - Analyze Python application type (web app, API, CLI, service)
   - Identify frameworks in use (Django, Flask, FastAPI, etc.)
   - Review current security configuration and dependencies
   - Assess deployment environment (cloud, on-premise, containers)
   - Identify sensitive data flows and attack surfaces

2. **Python Security Tools Installation**
   - Install security scanning tools: `uv add --dev bandit safety semgrep`
   - Add dependency audit tools: `uv add --dev pip-audit`
   - Install static analysis: `uv add --dev mypy ruff`
   - Add secrets detection: `uv add --dev detect-secrets`
   - Install cryptography library: `uv add cryptography`

3. **Secure Dependency Management**
   ```toml
   # pyproject.toml security configuration
   [tool.uv]
   # Pin dependencies to specific versions
   requirement-files = ["requirements.txt"]

   [tool.pip-audit]
   # Configure dependency vulnerability scanning
   desc = true
   format = "json"
   output = "audit-report.json"
   ```
   - Pin all dependencies to specific versions
   - Regularly audit dependencies: `uv run pip-audit`
   - Set up automated vulnerability scanning in CI
   - Configure supply chain security checks

4. **Input Validation and Sanitization**
   ```python
   # Secure input validation patterns
   from pydantic import BaseModel, validator, Field
   from typing import Optional
   import html
   import re

   class SecureUserInput(BaseModel):
       username: str = Field(..., min_length=3, max_length=50)
       email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')

       @validator('username')
       def validate_username(cls, v):
           # Prevent XSS and injection attacks
           if not re.match(r'^[a-zA-Z0-9_-]+$', v):
               raise ValueError('Invalid username format')
           return html.escape(v)
   ```

5. **Framework-Specific Security Hardening**

   **Django Security Configuration:**
   ```python
   # settings.py security settings
   import os
   from pathlib import Path

   # Security settings
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   SECURE_SSL_REDIRECT = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   SECURE_CONTENT_TYPE_NOSNIFF = True
   SECURE_BROWSER_XSS_FILTER = True
   X_FRAME_OPTIONS = 'DENY'

   # CSRF protection
   CSRF_COOKIE_SECURE = True
   CSRF_COOKIE_HTTPONLY = True
   CSRF_COOKIE_SAMESITE = 'Strict'

   # Session security
   SESSION_COOKIE_SECURE = True
   SESSION_COOKIE_HTTPONLY = True
   SESSION_COOKIE_SAMESITE = 'Strict'
   SESSION_COOKIE_AGE = 3600  # 1 hour

   # Database security
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'OPTIONS': {
               'sslmode': 'require',
           },
       }
   }
   ```

   **Flask Security Configuration:**
   ```python
   # Flask security setup
   from flask import Flask
   from flask_talisman import Talisman
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   app = Flask(__name__)

   # Security headers
   Talisman(app, {
       'force_https': True,
       'strict_transport_security': True,
       'content_security_policy': {
           'default-src': "'self'",
           'script-src': "'self'",
           'style-src': "'self' 'unsafe-inline'",
       }
   })

   # Rate limiting
   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"]
   )
   ```

   **FastAPI Security Configuration:**
   ```python
   # FastAPI security setup
   from fastapi import FastAPI, Depends, HTTPException, status
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   from fastapi.middleware.cors import CORSMiddleware
   from fastapi.middleware.trustedhost import TrustedHostMiddleware
   import jwt

   app = FastAPI()
   security = HTTPBearer()

   # Trusted hosts
   app.add_middleware(
       TrustedHostMiddleware,
       allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
   )

   # CORS configuration
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       allow_credentials=True,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   ```

6. **Secure Configuration Management**
   ```python
   # Secure environment configuration
   import os
   from pathlib import Path
   from cryptography.fernet import Fernet
   import keyring

   class SecureConfig:
       def __init__(self):
           self.encryption_key = os.environ.get('ENCRYPTION_KEY')
           if not self.encryption_key:
               raise ValueError("ENCRYPTION_KEY environment variable required")

       def get_secret(self, key: str) -> str:
           """Retrieve encrypted secret from environment or keyring"""
           encrypted_value = os.environ.get(f"{key}_ENCRYPTED")
           if encrypted_value:
               fernet = Fernet(self.encryption_key.encode())
               return fernet.decrypt(encrypted_value.encode()).decode()
           return keyring.get_password("myapp", key)

   # .env.example template
   # DATABASE_URL_ENCRYPTED=...
   # API_KEY_ENCRYPTED=...
   # JWT_SECRET_ENCRYPTED=...
   ```

7. **Authentication and Authorization Security**
   ```python
   # Secure authentication implementation
   import bcrypt
   import jwt
   import secrets
   from datetime import datetime, timedelta
   from typing import Optional

   class SecureAuth:
       def __init__(self, secret_key: str):
           self.secret_key = secret_key
           self.algorithm = "HS256"

       def hash_password(self, password: str) -> str:
           """Securely hash password with bcrypt"""
           salt = bcrypt.gensalt(rounds=12)
           return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

       def verify_password(self, password: str, hashed: str) -> bool:
           """Verify password against hash"""
           return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

       def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
           """Create secure JWT token"""
           to_encode = data.copy()
           if expires_delta:
               expire = datetime.utcnow() + expires_delta
           else:
               expire = datetime.utcnow() + timedelta(minutes=15)

           to_encode.update({"exp": expire, "iat": datetime.utcnow()})
           return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
   ```

8. **SQL Injection Prevention**
   ```python
   # Secure database queries
   from sqlalchemy import text
   from sqlalchemy.orm import Session

   # ✅ Secure: Use parameterized queries
   def get_user_secure(db: Session, user_id: int):
       return db.execute(
           text("SELECT * FROM users WHERE id = :user_id"),
           {"user_id": user_id}
       ).fetchone()

   # ✅ Secure: Use ORM
   def get_user_orm(db: Session, user_id: int):
       return db.query(User).filter(User.id == user_id).first()

   # ❌ Vulnerable: Never use string formatting
   # def get_user_vulnerable(db: Session, user_id: int):
   #     return db.execute(f"SELECT * FROM users WHERE id = {user_id}")
   ```

9. **XSS and CSRF Protection**
   ```python
   # XSS prevention
   import html
   import bleach
   from markupsafe import Markup

   def sanitize_html_input(content: str) -> str:
       """Sanitize HTML content to prevent XSS"""
       allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
       allowed_attributes = {}
       return bleach.clean(content, tags=allowed_tags, attributes=allowed_attributes)

   def escape_user_input(user_input: str) -> str:
       """Escape user input for safe display"""
       return html.escape(user_input, quote=True)

   # CSRF protection (framework-specific implementation)
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)  # Flask
   ```

10. **Cryptography and Secrets Management**
    ```python
    # Secure cryptography implementation
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import secrets
    import base64

    class SecureCrypto:
        @staticmethod
        def generate_key() -> bytes:
            """Generate secure random key"""
            return secrets.token_bytes(32)

        @staticmethod
        def encrypt_data(data: bytes, key: bytes) -> bytes:
            """Encrypt data using AES-GCM"""
            iv = secrets.token_bytes(12)
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            return iv + encryptor.tag + ciphertext

        @staticmethod
        def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
            """Decrypt AES-GCM encrypted data"""
            iv = encrypted_data[:12]
            tag = encrypted_data[12:28]
            ciphertext = encrypted_data[28:]
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            return decryptor.update(ciphertext) + decryptor.finalize()
    ```

11. **Security Scanning and Static Analysis**
    ```toml
    # pyproject.toml security tools configuration
    [tool.bandit]
    exclude_dirs = ["tests", "migrations"]
    skips = ["B101"]  # Skip assert_used test

    [tool.semgrep]
    config = ["auto", "security-audit"]

    [tool.ruff]
    select = [
        "S",    # bandit security rules
        "B",    # flake8-bugbear
        "E",    # pycodestyle errors
        "F",    # pyflakes
    ]

    [tool.detect-secrets]
    exclude_files = "poetry.lock|\.secrets\.baseline$"
    ```

12. **Security Testing and CI Integration**
    ```yaml
    # .github/workflows/security.yml
    name: Security Checks
    on: [push, pull_request]

    jobs:
      security:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.11'

          - name: Install uv
            run: pip install uv

          - name: Install dependencies
            run: uv sync --dev

          - name: Run Bandit security scan
            run: uv run bandit -r src/ -f json -o bandit-report.json

          - name: Run Safety dependency check
            run: uv run safety check --json --output safety-report.json

          - name: Run Semgrep security analysis
            run: uv run semgrep --config=auto src/

          - name: Check for secrets
            run: uv run detect-secrets scan --all-files
    ```

13. **Security Monitoring and Logging**
    ```python
    # Secure logging configuration
    import logging
    import json
    from datetime import datetime
    from typing import Dict, Any

    class SecurityLogger:
        def __init__(self):
            self.logger = logging.getLogger('security')
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        def log_security_event(self, event_type: str, details: Dict[str, Any],
                              user_id: str = None, ip_address: str = None):
            """Log security events for monitoring"""
            event = {
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': event_type,
                'user_id': user_id,
                'ip_address': ip_address,
                'details': details
            }
            self.logger.warning(f"SECURITY_EVENT: {json.dumps(event)}")

    # Usage examples
    security_logger = SecurityLogger()
    security_logger.log_security_event(
        'failed_login_attempt',
        {'attempts': 3, 'locked': True},
        user_id='user123',
        ip_address='192.168.1.1'
    )
    ```

14. **Production Security Checklist**
    - [ ] All secrets stored securely (environment variables, key management service)
    - [ ] HTTPS enforced with proper TLS configuration
    - [ ] Security headers implemented (CSP, HSTS, etc.)
    - [ ] Input validation and output encoding in place
    - [ ] Authentication and authorization properly configured
    - [ ] SQL injection and XSS protection implemented
    - [ ] CSRF protection enabled
    - [ ] Rate limiting configured
    - [ ] Security logging and monitoring active
    - [ ] Dependencies regularly updated and scanned
    - [ ] Static security analysis in CI/CD pipeline
    - [ ] Penetration testing completed
    - [ ] Incident response plan documented

15. **Security Scripts and Automation**
    ```toml
    # Add security scripts to pyproject.toml
    [tool.uv.scripts]
    security-scan = "bandit -r src/"
    dependency-audit = "pip-audit"
    secrets-check = "detect-secrets scan --all-files"
    security-full = ["security-scan", "dependency-audit", "secrets-check"]
    security-fix = "semgrep --autofix --config=auto src/"
    ```

Remember to regularly update security dependencies, conduct security reviews, and stay informed about the latest Python security best practices and vulnerabilities.
