"""Collecthive Pytest conftest."""

from unittest.mock import patch

import pytest
from flask import Flask
from flask_inertia.unittest import InertiaTestResponse
from mongomock import MongoClient

import collecthive.app


@pytest.fixture()
def app() -> Flask:
    class PyMongoMock(MongoClient):
        def init_app(self, app):
            return super().__init__()

    with patch.object(collecthive.app, "mongo", PyMongoMock()):
        app_ = collecthive.app.create_app("test")
        app_.response_class = InertiaTestResponse
        yield app_


@pytest.fixture()
def client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
