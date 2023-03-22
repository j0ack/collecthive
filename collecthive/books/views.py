"""Books collectibles."""
from typing import List

from flask import Blueprint, Response
from flask_inertia import render_inertia
from pydantic import parse_obj_as

from collecthive.app import mongo
from collecthive.books.models import BookModel

books_bp = Blueprint("books", __name__)


@books_bp.route("/", methods=["GET"])
def index() -> Response:
    books = parse_obj_as(List[BookModel], list(mongo.db.books.find()))
    data = [book.dict() for book in books]
    return render_inertia("books/Index", props={"books": data})


@books_bp.route("/", methods=["POST"])
def create_book() -> Response:
    pass


@books_bp.route("/<int:book_id>/", methods=["PUT", "DELETE"])
def update_or_delete_book(book_id: int) -> Response:
    pass


@books_bp.route("/<string:isbn>/", methods=["DELETE"])
def get_book_info_from_isbn(isbn: str) -> Response:
    pass
