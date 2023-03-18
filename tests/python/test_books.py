import pytest
from flask import url_for
from pydantic_factories import ModelFactory

from collecthive.books.models import BookModel


class BookFactory(ModelFactory):
    __model__ = BookModel


@pytest.fixture()
def book(app):
    from collecthive.app import mongo

    book = dict(BookFactory.build())
    book_id = mongo.db.books.insert_one(book).inserted_id
    book.id = book_id

    yield book

    mongo.db.books.drop()


@pytest.fixture()
def books(app):
    from collecthive.app import mongo

    books = [dict(BookFactory.build()) for __ in range(1000)]
    breakpoint()
    mongo.db.books.insert_many(books)

    yield books

    mongo.db.books.drop()


def test_book_index(client, books):
    response = client.get(url_for("books.index"))
    data = response.inertia("app")
    assert data.component == "books/Index"
    assert len(data.props.books) == 1000
