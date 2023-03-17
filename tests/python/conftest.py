"""Collecthive Pytest conftest."""

import pytest
from flask import Flask
from flask_inertia.unittest import InertiaTestResponse

from collecthive.app import create_app


@pytest.fixture()
def app() -> Flask:
    app_ = create_app("test")
    app_.response_class = InertiaTestResponse
    return app_


@pytest.fixture()
def client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
