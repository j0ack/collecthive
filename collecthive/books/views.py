"""Books collectibles."""
import math
from pathlib import Path
from typing import Any, Dict, List

from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    flash,
    redirect,
    request,
    url_for,
)
from flask_inertia import render_inertia
from pydantic import ValidationError, parse_obj_as

from collecthive.app import mongo
from collecthive.books.helpers import get_book_metadata_from_isbn
from collecthive.books.models import BookModel
from collecthive.exceptions import parse_validation_error

books_bp = Blueprint("books", __name__)


@books_bp.route("/", methods=["GET"])
def index() -> Response:
    books = parse_obj_as(List[BookModel], list(mongo.db.books.find()))
    data = [book.dict() for book in books]

    per_page = current_app.config["ITEMS_PER_PAGE"]
    number_of_pages = math.ceil(len(data) / per_page)

    page = min(max(int(request.args.get("page", 1)), 1), number_of_pages)
    items = data[(page - 1) * per_page : page * per_page]  # noqa: E203
    pages = [page + 1 for page in range(number_of_pages)]

    return render_inertia(
        "books/Index",
        props={
            "books": items,
            "pages": pages,
            "current_page": page,
        },
    )


@books_bp.route("/<string:isbn>/", methods=["GET"])
def book_detail(isbn: str) -> Response:
    book_data = mongo.db.books.find_one({"isbn": isbn})
    if not book_data:
        abort(404)

    book = BookModel.parse_obj(book_data)
    return render_inertia("books/BookDetail", props={"book": book.dict()})


@books_bp.route("/create/", methods=["GET", "POST"])
def create_book() -> Response:
    if request.method == "POST":
        return create_book_post()
    else:
        return create_book_get()


def parse_book_form() -> Dict[str, Any]:
    """Parse book form."""
    data = {
        "authors": [],
    }
    for key, value in request.form.items():
        if key.startswith("authors"):
            data["authors"].append(value)
        else:
            data[key] = value

    return data


def save_book_cover(book: BookModel) -> None:
    """Save book cover from form data."""
    cover_file = request.files.get("coverFile")
    if cover_file:
        filepath = Path(cover_file.filename)
        filename = f"books/{book.isbn}{''.join(filepath.suffixes)}"
        mongo.save_file(filename, cover_file)
        book.cover = url_for("uploads", filename=filename)


def create_book_post() -> Response:
    """Create book in db."""
    data = parse_book_form()
    page_data = {"errors": {}}
    try:
        book = BookModel.parse_obj(data)
        save_book_cover(book)

        if mongo.db.books.find_one({"isbn": book.isbn}) is not None:
            msg = "ISBN already exists"
            raise ValueError(msg)

        mongo.db.books.insert_one(book.dict())
        flash("Book created", "success")
        return redirect(url_for("books.index"))
    except ValidationError as err:
        page_data["errors"] = parse_validation_error(err)
    except ValueError as err:
        page_data["errors"] = {"isbn": str(err)}

    return render_inertia("books/CreateBook", props=page_data)


def create_book_get() -> Response:
    """Get book form creation."""
    page_data = {
        "errors": None,
        "book": None,
    }
    isbn = request.args.get("isbn")
    if isbn:
        try:
            book = get_book_metadata_from_isbn(isbn)

            if mongo.db.books.find_one({"isbn": book.isbn}) is not None:
                msg = "ISBN already exists"
                raise ValueError(msg)

            page_data["book"] = book.dict()
        except ValidationError as err:
            page_data["errors"] = parse_validation_error(err)
        except ValueError as err:
            page_data["errors"] = {"isbn": str(err)}

    return render_inertia("books/CreateBook", props=page_data)


@books_bp.route("/<string:isbn>/", methods=["DELETE"])
def delete_book(isbn: str) -> Response:
    """Delete book from db."""
    result = mongo.db.books.delete_one({"isbn": isbn})
    if result.deleted_count == 0:
        abort(404)

    flash("Book deleted", "success")
    return redirect(url_for("books.index"))


@books_bp.route("/edit/<string:isbn>/", methods=["GET", "POST"])
def update_book(isbn: str) -> Response:
    """Update book info."""
    if request.method == "POST":
        return update_book_post(isbn)
    else:
        return update_book_get(isbn)


def update_book_get(isbn: str):
    book = mongo.db.books.find_one({"isbn": isbn})
    if not book:
        abort(404)

    return render_inertia("books/EditBook", props={"book": book.dict()})


def update_book_post(isbn: str) -> Response:
    page_data = {
        "errors": {},
        "book": {},
    }
    try:
        book_params = parse_book_form()
        page_data["book"] = book_params
        book = BookModel.parse_obj(book_params)
        save_book_cover(book)

        result = mongo.db.books.update_one({"isbn": isbn}, {"$set": book.dict()})
        if result.modified_count == 0:
            abort(404)

        flash("Book updated", "success")
        return redirect(url_for("books.book_detail", isbn=isbn))
    except ValidationError as err:
        page_data["errors"] = parse_validation_error(err)
        return render_inertia("books/EditBook", props=page_data)
