"""Books collectibles."""
import math
from typing import List

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


def create_book_post() -> Response:
    """Create book in db."""
    data = {
        "authors": [],
    }
    for key, value in request.form.items():
        if key.startswith("authors"):
            data["authors"].append(value)
        else:
            data[key] = value

    try:
        cover_file = request.files.get("coverFile")
        book = BookModel.parse_obj(data)
        book.save_cover(cover_file)

        # if mongo.db.books.find_one({"isbn": book.isbn}) is not None:
        #     raise ValidationError({
        #         "loc": ("isbn",),
        #         "msg": "ISBN already exists",
        #    })

        mongo.db.books.insert_one(book.dict())
        flash("Book created", "success")
        return redirect(url_for("books.index"))
    except ValidationError as err:
        inertia_errors = {}
        for error in err.errors():
            key = error["loc"][0]
            value = error["msg"]
            inertia_errors[key] = value

        page_data = {"errors": inertia_errors}
        return render_inertia("books/CreateBook", props=page_data)


def create_book_get() -> Response:
    """Get book form creation."""
    page_data = {}
    isbn = request.args.get("isbn")
    if isbn:
        try:
            book = get_book_metadata_from_isbn(isbn)
            page_data["book"] = book.dict()
        except Exception as err:
            page_data["errors"] = str(err)

    return render_inertia("books/CreateBook", props=page_data)


@books_bp.route("/<int:book_id>/", methods=["PUT", "DELETE"])
def update_or_delete_book(book_id: int) -> Response:
    pass
