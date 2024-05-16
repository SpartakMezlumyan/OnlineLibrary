from pony import orm

db = orm.Database()


class Author(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    first_name = orm.Required(str)
    last_name = orm.Required(str)
    books = orm.Set('Book')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Book(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    description = orm.Required(str)
    count = orm.Required(int, sql_default=1)
    author = orm.Required(Author)

    codes = orm.Set('Code')


class Code(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    hash = orm.Required(str)
    book = orm.Required(Book)


db.bind(provider='sqlite', filename='library.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
