from flask import url_for


def test_index(client):
    response = client.get(url_for("index"))
    data = response.inertia("app")
    assert data.component == "Index"
