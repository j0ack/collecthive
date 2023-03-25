"""Books Pydantic models."""
from enum import Enum
from pathlib import Path
from typing import IO, List, Optional

from flask import current_app, url_for
from pydantic import validator
from werkzeug.utils import secure_filename

from collecthive.models import CollectHiveModel

BOOK_COVER_DIR = "books"


class BookStatus(str, Enum):

    in_stock = "in_stock"
    wishlist = "wishlist"


class BookModel(CollectHiveModel):

    title: str = ""
    subtitle: Optional[str] = None
    isbn: str = ""
    authors: List[str] = []
    description: Optional[str] = None
    edition: str = ""
    cover: Optional[str] = None
    status: BookStatus = BookStatus.in_stock

    @validator("isbn")
    def validate_isbn(cls, value):
        """Validate ISBN field and transform it to canonical ISBN."""
        from collecthive.books.helpers import validate_isbn_number

        canonical_isbn = validate_isbn_number(value)
        return canonical_isbn

    def save_cover(self, cover_file: Optional[IO]):
        """Save book cover file and update `cover` attr."""
        if not cover_file:
            return

        folder = current_app.config["UPLOAD_DIR"] / BOOK_COVER_DIR
        folder.mkdir(parents=True, exist_ok=True)
        filename = Path(secure_filename(cover_file.filename))
        extensions = filename.suffixes
        output_filename = f"{self.isbn}{''.join(extensions)}"

        cover_file.save(folder / output_filename)
        self.cover = url_for("uploads", folder=BOOK_COVER_DIR, filename=output_filename)
