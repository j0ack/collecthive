from http import HTTPStatus
from unittest.mock import patch

import pytest
from faker import Faker
from faker.providers import isbn
from flask import url_for
from pydantic_factories import Ignore, ModelFactory

from collecthive.books.models import BookModel

fake = Faker()
fake.add_provider(isbn)


class BookFactory(ModelFactory):
    __model__ = BookModel
    __faker__ = fake

    id = Ignore()
    isbn = lambda: fake.isbn10()  # noqa: E731


@pytest.fixture()
def books_db():
    from collecthive.app import mongo

    yield mongo.db.books

    mongo.db.books.drop()


@pytest.fixture()
def book(app, books_db):
    book = BookFactory.build()
    book_id = books_db.insert_one(book.dict()).inserted_id
    book.id = book_id
    return book


@pytest.fixture()
def books(app, books_db):
    breakpoint()
    books = [book.dict() for book in BookFactory.batch(1000)]
    books_db.insert_many(books)
    return books


class TestBookList:
    @pytest.mark.parametrize(
        "page,expected_page,books_indexes",
        [
            (None, 1, (0, 5)),
            (1, 1, (0, 5)),
            (0, 1, (0, 5)),
            (201, 200, (995, 1000)),
            (100, 100, (495, 500)),
        ],
    )
    def test_book_index(self, client, books, page, expected_page, books_indexes):
        params = {}
        if page:
            params["page"] = page

        response = client.get(url_for("books.index", **params))

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/Index"
        assert len(data.props.books) == 5
        assert data.props.current_page == expected_page
        assert len(data.props.pages) == 200

        isbns = [book.isbn for book in data.props.books]
        expected_isbns = [
            book["isbn"] for book in books[books_indexes[0] : books_indexes[1]]  # noqa
        ]
        assert isbns == expected_isbns


class TestGetBook:
    @pytest.mark.parametrize(
        "with_book,status",
        [
            (True, HTTPStatus.OK),
            (False, HTTPStatus.NOT_FOUND),
        ],
    )
    def test_get_book(self, client, with_book, status, request):
        if with_book:
            book = request.getfixturevalue("book")
        else:
            book = BookFactory.build()

        response = client.get(url_for("books.book_detail", isbn=book.isbn))

        assert response.status_code == status

        if status == HTTPStatus.OK:
            data = response.inertia("app")
            assert data.component == "books/BookDetail"
            assert data.props.book.id == str(book.id)
            assert data.props.book.isbn == book.isbn


class TestCreateBook:
    def test_create_book_get(self, client):
        response = client.get(url_for("books.create_book"))

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/CreateBook"
        assert not hasattr(data.props, "book")

    def test_create_book_get_with_metadata(self, client, book):
        with patch(
            "collecthive.books.views.get_book_metadata_from_isbn",
            return_value=book,
        ):
            response = client.get(url_for("books.create_book", isbn=book.isbn))

            assert response.status_code == HTTPStatus.OK

            data = response.inertia("app")
            assert data.component == "books/CreateBook"
            assert data.props.book.isbn == book.isbn

    def test_create_book_get_with_metadata_errors(self, client, book):
        with patch(
            "collecthive.books.views.get_book_metadata_from_isbn",
            side_effect=ValueError(),
        ):
            response = client.get(url_for("books.create_book", isbn=book.isbn))

            assert response.status_code == HTTPStatus.OK

            data = response.inertia("app")
            assert data.component == "books/CreateBook"
            assert not hasattr(data.props, "book")
            assert hasattr(data.props, "errors")

    def test_create_book_post(self, client, books_db):
        book = BookFactory.build()
        query_book_data = {
            "title": "Lorem ipsum",
            "subtitle": "Dolor est",
            "isbn": book.isbn,
            "authors[0]": "John Doe",
            "authors[1]": "Jane Doe",
            "description": "Ut enim ad minim veniam, quis nostrud exercitation.",
            "edition": "Stratacard",
            "cover": None,
            "status": "in_stock",
        }
        response = client.post(
            url_for("books.create_book"),
            data=query_book_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/Index"
        book_data = data.props.books[-1]
        assert book_data.title == "Lorem ipsum"
        assert book_data.subtitle == "Dolor est"
        assert book_data.isbn == book.isbn
        assert book_data.authors == ["John Doe", "Jane Doe"]
        assert (
            book_data.description
            == "Ut enim ad minim veniam, quis nostrud exercitation."  # noqa: W503
        )
        assert book_data.edition == "Stratacard"
        assert book_data.cover is None
        assert book_data.status == "in_stock"

        assert data.props.messages == ["Book created"]

    @pytest.mark.parametrize(
        "data,field",
        [
            (
                {
                    "title": "Lorem ipsum",
                    "subtitle": "Dolor est",
                    "isbn": "123456",  # invalid isbn
                    "authors[0]": "John Doe",
                    "authors[1]": "Jane Doe",
                    "description": "Ut enim ad minim veniam, quis nostrud exercitation.",
                    "edition": "Stratacard",
                    "cover": None,
                    "status": "in_stock",
                },
                "isbn",
            ),
            (
                {
                    "title": "Lorem ipsum",
                    "subtitle": "Dolor est",
                    "isbn": "123456",  # invalid isbn
                    "description": "Ut enim ad minim veniam, quis nostrud exercitation.",
                    "edition": "Stratacard",
                    "cover": None,
                    "status": "invalid_status",
                },
                "status",
            ),
        ],
    )
    def test_create_book_post_invalid_data(self, client, books_db, data, field):
        response = client.post(
            url_for("books.create_book"),
            data=data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/CreateBook"
        assert hasattr(data.props, "errors")
        assert hasattr(data.props.errors, field)

    def test_create_book_post_isbn_already_exists(self, client, book):
        query_book = {
            "title": "Lorem ipsum",
            "subtitle": "Dolor est",
            "isbn": book.isbn,
            "authors[0]": "John Doe",
            "authors[1]": "Jane Doe",
            "description": "Ut enim ad minim veniam, quis nostrud exercitation.",
            "edition": "Stratacard",
            "cover": None,
            "status": "in_stock",
        }
        response = client.post(
            url_for("books.create_book"),
            data=query_book,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/CreateBook"
        assert data.props.errors.isbn == "ISBN already exists"


def test_update_book(client):
    pass


def test_delete_book(client):
    pass
