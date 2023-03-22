enum BookStatus {
    in_stock = "in_stock",
    wishlist = "wishlist",
}

interface Book {
    title: string;
    subtitle?: string;
    isbn: string;
    authors: Array<string>;
    description?: string;
    editions: Array<string>;
    cover?: string;
    status: BookStatus;
}
