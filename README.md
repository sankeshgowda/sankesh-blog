# Sankesh Blog

A production-ready Medium, Hashnode, and Dev.to inspired blogging platform built with Django 5, Bootstrap 5, CKEditor 5, Crispy Forms, AllAuth, Pillow, and Taggit-ready dependencies.

## Folder Structure

```text
sankesh_blog/
  accounts/       Profile management and user profile signals
  analytics/      Staff analytics overview
  blog/           Posts, categories, tags, comments, likes, bookmarks
  dashboard/      Author dashboard, CRUD, bookmarks, analytics
  newsletter/     Newsletter subscribers
  config/         Settings, URLs, ASGI, WSGI
  templates/      Public, auth, dashboard templates
  static/         CSS and JavaScript assets
  media/          Uploaded files in development
```

## Local Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## Main Features

- AllAuth registration, login, logout, password reset, and email verification.
- Profile management with avatar, bio, and social links.
- Post creation, editing, deletion, drafts, scheduled publishing, CKEditor rich text, featured images, categories, tags, search, and pagination.
- Nested comments data model, likes, bookmarks, social sharing, related posts, and author profiles.
- View tracking, popular/trending posts, user dashboard statistics, and Chart.js dashboard charts.
- Automatic reading time, summary generation, and SEO suggestions.
- Responsive glassmorphism UI with dark/light mode, sticky navbar, hero slider, loading screen, animations, and scroll-to-top.

## Database

SQLite works out of the box. For MySQL, install system MySQL client headers if needed, create a UTF-8 database, then update `.env`:

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=sankesh_blog
DB_USER=sankesh_user
DB_PASSWORD=strong-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

The models avoid SQLite-only fields and use indexes/constraints that are MySQL compatible.

## Deployment Checklist

1. Set `DEBUG=False`.
2. Set a strong `SECRET_KEY`.
3. Add production domains to `ALLOWED_HOSTS`.
4. Add HTTPS origins to `CSRF_TRUSTED_ORIGINS`.
5. Configure real SMTP settings and set `ACCOUNT_EMAIL_VERIFICATION=mandatory`.
6. Set `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, and `CSRF_COOKIE_SECURE=True`.
7. Run:

```bash
python manage.py collectstatic
python manage.py migrate
gunicorn config.wsgi:application
```

8. Serve static files through WhiteNoise or your web server, and serve media from durable object storage in production.

## Security Notes

Django CSRF, password hashing, ORM parameterization, XSS-aware template escaping, Clickjacking protection, secure file upload handling through `ImageField`, and conservative security headers are enabled. Keep `post.content|safe` limited to trusted authors or add HTML sanitization before opening publishing to untrusted users.
