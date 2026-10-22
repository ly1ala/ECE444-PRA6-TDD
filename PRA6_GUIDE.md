# PRA6 setup and demonstration

Adapted from https://github.com/shuruizUofT/flaskr-tdd; upstream LICENSE retained.

## Run locally

Use Python 3.9 or newer (local verification used Python 3.9).

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python create_db.py
python -m flask --app project.app run --port 5001
```

Open http://localhost:5001. Local credentials default to admin/admin.
Tests use a separate temporary SQLite database for each test. They do not reset the application database.

## Changes from course code

- Added create_app(test_config) so database configuration is applied before SQLAlchemy initialization.
- Removed the test fixture's reliance on a shared database and strengthened deletion tests to assert database contents.
- Added search tests for title/body matches, case insensitivity, empty queries, no matches, and correct result IDs.
- Added tests that unauthenticated add/delete requests return 401 and do not mutate data.
- Fixed search.html to use entry.id rather than nonexistent entry.post_id.
- Added environment variables APP_USERNAME, APP_PASSWORD, SECRET_KEY.

## Deploy to Render

1. Upload these files to your own GitHub repository, keeping project/, tests/, and .github/ directories intact. Do not upload the containing folder as an extra directory.
2. Sign into Render using your UofT account as instructed by the assignment.
3. Create a Free Postgres database. Create a Free Python web service from your repo in the same region.
4. Set build command: `pip install -r requirements.txt`.
5. Set start command: `python create_db.py && gunicorn project.app:app --bind 0.0.0.0:$PORT`.
6. Set DATABASE_URL to the database Internal Database URL. Keep that value private.
7. Set APP_USERNAME and APP_PASSWORD to your demonstration credentials; set SECRET_KEY to a long random secret. Do not commit these values.
8. Select a supported Python version and use that same version locally for a final test run. The runtime.txt inherited from upstream requests 3.12.0; configure PYTHON_VERSION in Render explicitly if required.
9. Deploy, inspect logs, then open the resulting HTTPS URL. A successful build alone does not verify the application.
10. Verify homepage, failed login, successful login, add a uniquely titled post, search by title and text, log out, and confirm protected actions are refused. Log in and click a post to delete it. Add another post and verify it remains after a redeploy.

Render free services lose local SQLite files on restart/redeploy, so use Postgres. Current Render documentation says free Postgres expires after 30 days; upstream's 90-day statement is outdated. Check the dashboard expiration before your TA session.
Sources: https://render.com/docs/deploy-flask and https://render.com/docs/free

## Explain to the TA

- Red/Green/Refactor: write a behavior test, observe an appropriate failure, implement the behavior, and improve structure while tests remain green. Adding passing tests to an existing app does not prove a historical TDD cycle.
- A fixture prepares a known database, yields a test client, then removes the session and tables. A fresh temporary path isolates each test.
- test_index checks HTTP 200; test_database checks the configured SQLite file exists; test_empty_db checks the empty-state text.
- test_login_logout covers successful login/logout and invalid username/password. Flask stores a signed session cookie; SECRET_KEY signs it.
- test_messages logs in, posts form data, follows the redirect, and checks rendered content. Titles are escaped; the tutorial deliberately renders body HTML using safe. This is a tutorial feature with an XSS risk, not a production-safe rich-text implementation.
- Deletion tests check actual database state, not just a success message. Unauthorized tests show rejected requests leave rows unchanged.
- Search tests insert known rows and check included/excluded results for title/body matches and case insensitivity. The current tutorial filters results in the template.
- create_app applies test configuration before db.init_app; changing the URI afterward does not rebind an existing engine.
- Flask routes map requests to functions; Jinja renders HTML; SQLAlchemy models map Python objects to rows; commit persists changes; Gunicorn serves the WSGI app.
- DATABASE_URL selects Postgres in hosting and SQLite locally. create_db.py creates missing tables; it is not a schema migration system.
- The course app deletes via GET and accepts raw body HTML. Explain these tutorial limitations if asked; production would use authenticated state-changing POST/DELETE requests, CSRF protection, and safe HTML handling.

## Submission

Submit https://github.com/ly1ala/ECE444-PRA6-TDD to Quercus. Attend your assigned PRA and have the TA verify the deployment and ask about your tests before the session ends.

## Verified status

13 tests passed locally, and GitHub Actions passed tests, Black, and Flake8. Code is published at the repository above. The live Render app at https://ece444-pra6-tdd-1rrg.onrender.com/ was verified for homepage, failed/successful login, posting, search, deletion, logout, and unauthorized deletion protection on October 22, 2026. The hosting database is PostgreSQL; keep its connection credentials private.
