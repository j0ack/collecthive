"""Books Pydantic models."""

from enum import Enum
from typing import List, Optional

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
    editions: List[str] = []
    cover: Optional[str] = None
    status: BookStatus = BookStatus.in_stock
