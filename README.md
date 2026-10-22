# ECE444 PRA6 — TDD and Web App Deployment

A Flask blogging app for ECE444 PRA6. Users can view and search posts, log in and out, and add or delete posts while logged in.

Adapted from the [course tutorial](https://github.com/shuruizUofT/flaskr-tdd). The original MIT license is retained in LICENSE.

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python create_db.py
python -m flask --app project.app run --port 5001
```

Open http://localhost:5001. Default local login: `admin` / `admin`.

## Run tests

```sh
python -m pytest -v
```

The suite contains 13 cases covering the homepage, database, login/logout, posting, deletion, search, and login protection. Each test uses an isolated temporary SQLite database.

## Deploy on Render

- Build command: `pip install -r requirements.txt`
- Start command: `python create_db.py && gunicorn project.app:app --bind 0.0.0.0:$PORT`
- Set `DATABASE_URL` to your PostgreSQL connection URL.
- Set `SECRET_KEY`, `APP_USERNAME`, and `APP_PASSWORD` privately in Render.
- Without `DATABASE_URL`, the app uses local SQLite at `project/flaskr.db`.

See [PRA6_GUIDE.md](PRA6_GUIDE.md) for deployment instructions, test explanations, and the TA demonstration checklist. Deployment is not yet verified.

## Project files

- `project/`: routes, database model, HTML templates, CSS, and JavaScript.
- `tests/`: automated tests.
- `create_db.py`: creates database tables.
- `requirements.txt`, `Procfile`, `runtime.txt`: dependencies and deployment configuration.
- `.github/workflows/test.yml`: GitHub test workflow.
- `.gitignore`: excludes virtual environments, local databases, caches, and secrets.
