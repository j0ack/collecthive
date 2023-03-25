export const BOOK_STATUSES = ['in_stock', 'wishlist'] as const;
type BookStatus = typeof BOOK_STATUSES[number];
