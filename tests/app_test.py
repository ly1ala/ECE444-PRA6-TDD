from pathlib import Path

import pytest

from project.app import create_app, db
from project.models import Post


@pytest.fixture
def client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
            "SECRET_KEY": "test-secret",
        }
    )
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def login(client, username, password):
    """Login helper function"""
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )


def logout(client):
    """Logout helper function"""
    return client.get("/logout", follow_redirects=True)


def test_index(client):
    response = client.get("/", content_type="html/text")
    assert response.status_code == 200


def test_database(client):
    """initial test. ensure that the database exists"""
    tester = Path(db.engine.url.database).is_file()
    assert tester


def test_empty_db(client):
    """Ensure database is blank"""
    rv = client.get("/")
    assert b"No entries yet. Add some!" in rv.data


def test_login_logout(client):
    """Test login and logout using helper functions"""
    rv = login(
        client,
        client.application.config["USERNAME"],
        client.application.config["PASSWORD"],
    )
    assert b"You were logged in" in rv.data
    rv = logout(client)
    assert b"You were logged out" in rv.data
    rv = login(
        client,
        client.application.config["USERNAME"] + "x",
        client.application.config["PASSWORD"],
    )
    assert b"Invalid username" in rv.data
    rv = login(
        client,
        client.application.config["USERNAME"],
        client.application.config["PASSWORD"] + "x",
    )
    assert b"Invalid password" in rv.data


def test_messages(client):
    """Ensure that user can post messages"""
    login(
        client,
        client.application.config["USERNAME"],
        client.application.config["PASSWORD"],
    )
    rv = client.post(
        "/add",
        data=dict(title="<Hello>", text="<strong>HTML</strong> allowed here"),
        follow_redirects=True,
    )
    assert b"No entries yet. Add some!" not in rv.data
    assert b"&lt;Hello&gt;" in rv.data
    assert b"<strong>HTML</strong> allowed here" in rv.data


def test_delete_message(client):
    login(client, "admin", "admin")
    client.post("/add", data={"title": "Delete me", "text": "body"})
    post_id = db.session.query(Post).one().id
    rv = client.get(f"/delete/{post_id}")
    assert rv.get_json()["status"] == 1
    assert db.session.get(Post, post_id) is None


def test_add_requires_login(client):
    response = client.post("/add", data={"title": "Blocked", "text": "body"})
    assert response.status_code == 401
    assert db.session.query(Post).count() == 0


def test_delete_requires_login(client):
    post = Post("Keep me", "body")
    db.session.add(post)
    db.session.commit()
    post_id = post.id
    response = client.get(f"/delete/{post_id}")
    assert response.status_code == 401
    assert response.get_json()["status"] == 0
    assert db.session.get(Post, post_id) is not None


@pytest.mark.parametrize("query", ["ALPHA", "needle"])
def test_search_matches_title_or_body(client, query):
    db.session.add_all([Post("Alpha", "contains needle"), Post("Unrelated", "other")])
    db.session.commit()
    response = client.get("/search/", query_string={"query": query})
    assert response.status_code == 200
    assert b"Alpha" in response.data
    assert b"Unrelated" not in response.data


@pytest.mark.parametrize("query", ["", "missing-term"])
def test_search_empty_or_no_match(client, query):
    db.session.add(Post("Hidden post", "body"))
    db.session.commit()
    response = client.get("/search/", query_string={"query": query})
    assert response.status_code == 200
    assert b"Hidden post" not in response.data


def test_search_result_uses_post_id(client):
    db.session.add(Post("Find me", "body"))
    db.session.commit()
    post_id = db.session.query(Post).one().id
    response = client.get("/search/", query_string={"query": "Find me"})
    assert f'id="{post_id}"'.encode() in response.data
