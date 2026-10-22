# ECE444 PRA6 — TDD and Web App Deployment

A Flask blogging app for ECE444 PRA6. Users can view and search posts, log in and out, and add or delete posts while logged in.

Adapted from the [course tutorial](https://github.com/shuruizUofT/flaskr-tdd). The original MIT license is retained in LICENSE.

## Open the website

### Render website

Click [Open the live website](https://ece444-pra6-tdd-1rrg.onrender.com/) or [Open the login page](https://ece444-pra6-tdd-1rrg.onrender.com/login).

The public website does not require running the app on your computer. After the free service becomes idle, the first visit may take about a minute to load.

Hosted on Render with PostgreSQL. Use username `admin` and the current password configured privately in Render (`APP_PASSWORD`). Do not publish the password in this repository.

### Local website

Open this project folder in VS Code, then open **Terminal → New Terminal**. Run the following commands from the project root on macOS/Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python create_db.py
python -m flask --app project.app run --port 5001
```

Open [the local website](http://localhost:5001/) in your browser. Keep the terminal running; press **Ctrl+C** to stop the server. The default local login is `admin` / `admin`, unless you set `APP_USERNAME` or `APP_PASSWORD` in your terminal environment.

Local development uses SQLite by default. Local posts are separate from posts stored in the deployed PostgreSQL database.

For later visits, start the local server again from the project root:

```sh
source .venv/bin/activate
python -m flask --app project.app run --port 5001
```

### Render dashboard

The owner can sign in to [Render service dashboard](https://dashboard.render.com/web/srv-dbd5luo473hc73dghn40) to inspect deployment status and logs, or open [Environment settings](https://dashboard.render.com/web/srv-dbd5luo473hc73dghn40/env) to manage environment variables.

After pushing code updates to GitHub, select **Manual Deploy → Deploy latest commit** in the Render service dashboard. Wait for the status to show **Live**, then refresh the public website.

The Render dashboard requires account access; it is separate from the public website. A README-only update does not require redeploying the app.

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

See [PRA6_GUIDE.md](PRA6_GUIDE.md) for deployment instructions, test explanations, and the TA demonstration checklist. Homepage, login/logout, posting, search, deletion, and unauthorized deletion protection were verified on the live website on October 22, 2026.

## Project files

- `project/`: routes, database model, HTML templates, CSS, and JavaScript.
- `tests/`: automated tests.
- `create_db.py`: creates database tables.
- `requirements.txt`, `Procfile`, `runtime.txt`: dependencies and deployment configuration.
- `.github/workflows/test.yml`: GitHub test workflow.
- `.gitignore`: excludes virtual environments, local databases, caches, and secrets.
