from http import HTTPStatus
from io import BytesIO
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
    books = [book.dict() for book in BookFactory.batch(1000)]
    books_db.insert_many(books)
    return books


@pytest.fixture()
def cover_file():
    return (BytesIO(b"fake book cover"), "fake_image_file.jpg")


@pytest.fixture()
def book_form_data_factory():
    def _make_form_data(isbn: str):
        return {
            "isbn": isbn,
            "title": "Lorem ipsum",
            "subtitle": "Dolor est",
            "authors[0]": "John Doe",
            "authors[1]": "Jane Doe",
            "description": "Ut enim ad minim veniam, quis nostrud exercitation.",
            "edition": "Stratacard",
            "cover": None,
            "status": "in_stock",
        }

    return _make_form_data


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
        assert data.props.book is None
        assert data.props.errors is None

    def test_create_book_get_with_metadata(self, client):
        book = BookFactory.build()
        with patch(
            "collecthive.books.views.get_book_metadata_from_isbn",
            return_value=book,
        ):
            response = client.get(url_for("books.create_book", isbn=book.isbn))

            assert response.status_code == HTTPStatus.OK

            data = response.inertia("app")
            assert data.component == "books/CreateBook"
            assert data.props.book.isbn == book.isbn
            assert data.props.errors is None

    def test_create_book_get_with_metadata_already_exists(self, client, book):
        with patch(
            "collecthive.books.views.get_book_metadata_from_isbn",
            return_value=book,
        ):
            response = client.get(url_for("books.create_book", isbn=book.isbn))

            assert response.status_code == HTTPStatus.OK

            data = response.inertia("app")
            assert data.component == "books/CreateBook"
            assert data.props.book is None
            assert data.props.errors.isbn == "ISBN already exists"

    def test_create_book_get_with_metadata_errors(self, client, book):
        with patch(
            "collecthive.books.views.get_book_metadata_from_isbn",
            side_effect=ValueError("Test"),
        ):
            response = client.get(url_for("books.create_book", isbn=book.isbn))

            assert response.status_code == HTTPStatus.OK

            data = response.inertia("app")
            assert data.component == "books/CreateBook"
            assert data.props.book is None
            assert data.props.errors.isbn == "Test"

    def test_create_book_post(self, client, books_db, book_form_data_factory):
        book = BookFactory.build()
        book_form_data = book_form_data_factory(book.isbn)
        response = client.post(
            url_for("books.create_book"),
            data=book_form_data,
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

        assert ["success", "Book created"] in data.props.messages

    def test_create_book_post_with_cover(
        self, client, books_db, book_form_data_factory, cover_file
    ):
        book = BookFactory.build()
        book_form_data = book_form_data_factory(book.isbn)
        book_form_data["coverFile"] = cover_file
        response = client.post(
            url_for("books.create_book"),
            data=book_form_data,
            content_type="multipart/form-data",
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
        assert book_data.cover == f"/uploads/books/{book.isbn}.jpg"
        assert book_data.status == "in_stock"

        assert ["success", "Book created"] in data.props.messages

    @pytest.mark.parametrize(
        "data,field",
        [
            (
                {
                    "isbn": "123456",  # invalid isbn
                },
                "isbn",
            ),
            (
                {
                    "status": "invalid_status",  # invalid status
                },
                "status",
            ),
        ],
    )
    def test_create_book_post_invalid_data(
        self, client, books_db, book_form_data_factory, data, field
    ):
        book = BookFactory.build()
        book_form_data = book_form_data_factory(book.isbn)
        book_form_data.update(data)

        response = client.post(
            url_for("books.create_book"),
            data=book_form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/CreateBook"
        assert hasattr(data.props, "errors")
        assert hasattr(data.props.errors, field)

    def test_create_book_post_isbn_already_exists(
        self, client, book, book_form_data_factory
    ):
        book_form_data = book_form_data_factory(book.isbn)
        response = client.post(
            url_for("books.create_book"),
            data=book_form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/CreateBook"
        assert data.props.errors.isbn == "ISBN already exists"


class TestUpdateBook:
    def test_update_book(self, client, book, book_form_data_factory):
        book_form_data = book_form_data_factory(book.isbn)
        response = client.post(
            url_for("books.update_book", isbn=book.isbn),
            data=book_form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/BookDetail"
        assert ["success", "Book updated"] in data.props.messages

        book_data = data.props.book
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

    def test_update_inexistent_book(self, client, book_form_data_factory):
        book = BookFactory.build()
        book_form_data = book_form_data_factory(book.isbn)
        response = client.post(
            url_for("books.update_book", isbn=book.isbn),
            data=book_form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_book_invalid_data(self, client, book, book_form_data_factory):
        book_form_data = book_form_data_factory(book.isbn)
        book_form_data["status"] = "invalid"

        response = client.post(
            url_for("books.update_book", isbn=book.isbn),
            data=book_form_data,
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/EditBook"
        assert hasattr(data.props.errors, "status")

        book_data = data.props.book
        assert book_data.title == "Lorem ipsum"
        assert book_data.subtitle == "Dolor est"
        assert book_data.isbn == book.isbn
        assert book_data.authors == ["John Doe", "Jane Doe"]
        assert (
            book_data.description
            == "Ut enim ad minim veniam, quis nostrud exercitation."  # noqa: W503
        )
        assert book_data.edition == "Stratacard"
        assert book_data.status == "invalid"

    def test_update_book_cover(self, client, book, cover_file, book_form_data_factory):
        book_form_data = book_form_data_factory(book.isbn)
        book_form_data["coverFile"] = cover_file
        response = client.post(
            url_for("books.update_book", isbn=book.isbn),
            data=book_form_data,
            content_type="multipart/form-data",
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/BookDetail"
        book_data = data.props.book
        assert book_data.title == "Lorem ipsum"
        assert book_data.subtitle == "Dolor est"
        assert book_data.isbn == book.isbn
        assert book_data.authors == ["John Doe", "Jane Doe"]
        assert (
            book_data.description
            == "Ut enim ad minim veniam, quis nostrud exercitation."  # noqa: W503
        )
        assert book_data.edition == "Stratacard"
        assert book_data.cover == f"/uploads/books/{book.isbn}.jpg"
        assert book_data.status == "in_stock"

        assert ["success", "Book updated"] in data.props.messages

    def update_book_get(self, client, book):
        response = client.get(
            url_for("books.update_book", isbn=book.isbn),
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/EditBook"
        assert data.props.book.isbn == book.isbn

    def update_inexistent_book_get(self, client):
        book = BookFactory.build()
        response = client.get(
            url_for("books.update_book", isbn=book.isbn),
        )

        assert response.status_code == HTTPStatus.NOT_FOUND


class TestDeleteBook:
    def test_delete_book(self, client, book):
        response = client.delete(
            url_for("books.delete_book", isbn=book.isbn),
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.OK

        data = response.inertia("app")
        assert data.component == "books/Index"
        assert ["success", "Book deleted"] in data.props.messages

    def test_delete_book_invalid_isbn(self, client):
        book = BookFactory.build()
        response = client.delete(
            url_for("books.delete_book", isbn=book.isbn),
            follow_redirects=True,
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
