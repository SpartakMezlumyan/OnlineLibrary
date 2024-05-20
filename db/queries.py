from typing import List
from pony import orm
from db.base import Author, Book


@orm.db_session
def add_author(first_name: str, last_name: str) -> Author:
    return Author(
        first_name=first_name,
        last_name=last_name,
    )


@orm.db_session
def add_book(title: str, description: str, author: Author) -> Book:
    return Book(
        title=title,
        description=description,
        author=author
    )

@orm.db_session
def fetch_books() -> List[Book]:
    return Book.select().prefetch(Author).fetch()

for item in fetch_books():
    print(item.author.full_name())