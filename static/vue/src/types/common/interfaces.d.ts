interface Book {
    id?: string,
    title: string;
    subtitle?: string;
    isbn: string;
    authors: Array<string>;
    description?: string;
    edition: string;
    cover?: string;
    status: BookStatus;
}
