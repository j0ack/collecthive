"""Collecthive Pytest conftest."""

from mimetypes import guess_type
from unittest.mock import patch

import pytest
from flask import Flask
from flask_inertia.unittest import InertiaTestResponse
from gridfs import GridFS
from mongomock import MongoClient
from mongomock.gridfs import enable_gridfs_integration

import collecthive.app


@pytest.fixture(scope="session")
def app() -> Flask:
    class PyMongoMock(MongoClient):
        def init_app(self, app):
            enable_gridfs_integration()
            self.app = app
            return super().__init__()

        def save_file(self, filename, fileobj):
            storage = GridFS(self.db, "fs")
            content_type, __ = guess_type(filename)
            storage.put(fileobj, filename=filename, content_type=content_type)

        def send_file(self, filename):
            pass

    with patch.object(collecthive.app, "mongo", PyMongoMock()):
        app_ = collecthive.app.create_app("test")
        app_.response_class = InertiaTestResponse
        yield app_


@pytest.fixture(scope="session")
def client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
