import isbnlib

from collecthive.books.models import BookModel


def validate_isbn_number(isbn: str):
    """Validate ISBN number."""
    canonical_isbn = isbnlib.canonical(isbn)
    if isbnlib.notisbn(canonical_isbn):
        raise ValueError(f"{isbn} is not a valid ISBN")

    return canonical_isbn


def get_book_metadata_from_isbn(isbn: str) -> BookModel:
    """Get book metadata using isbnlib from its ISBN."""
    canonical_isbn = validate_isbn_number(isbn)
    metadata = isbnlib.meta(canonical_isbn)

    book_data = {
        "isbn": canonical_isbn,
        "title": metadata.get("Title", ""),
        "edition": metadata.get("Publisher", ""),
        "authors": metadata.get("Authors", []),
    }

    if cover := isbnlib.cover(canonical_isbn):
        book_data["cover"] = cover.get("thumbnail")

    return BookModel(**book_data)
