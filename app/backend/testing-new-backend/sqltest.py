import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class Base(orm.DeclarativeBase):
    pass

class User(Base):
    pass


class Post(Base):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
