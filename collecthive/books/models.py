"""Books Pydantic models."""
from enum import Enum
from typing import List, Optional

from pydantic import validator

from collecthive.models import CollectHiveModel


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
