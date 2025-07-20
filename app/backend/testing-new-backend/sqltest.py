import sqlalchemy as sa
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy import ForeignKey, String

engine = sa.create_engine("sqlite+pysqlite:///:memory:", echo=True)

class Base(orm.DeclarativeBase): pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    full_name: Mapped[str]

    sent_messages: Mapped[list["Post"]] = relationship(back_populates="author")

    received_messages: Mapped[list["Post"]] = relationship(back_populates="receiver")

    def __repr__(self) -> str:
        return f"<User id={self.id!r}, username={self.username!r}, full_name={self.full_name!r}>"


class Post(Base):
    __tablename__ = "post"


    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    time: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    sender_id = mapped_column(ForeignKey("user.id"))
    receiver_id = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship(back_populates="sent_messages")
    receiver: Mapped["User"] = relationship(back_populates="received_messages")

    def __repr__(self) -> str:
        return f"<Post id={self.id!r}, content={self.content!r} author={self.author.username!r}>"



def main():
    Base.metadata.create_all(engine)
    # test_user1 = User(username="test_user", full_name="Test User")
    # test_user2 = User(username="second_test_user")
    # test_post1 = Post(content="This is a Test Post", author=test_user1)
    # test_post2 = Post(content="This is another Test Post", author=test_user1)
    # test_post3 = Post(content="This is the third Test Post", author=test_user2)

    # print(test_user1)
    # print(test_user2)
    # print(test_post1)
    # print(test_post2)
    # print(test_post3, "\n")
    # print(test_user1.posts)
    # print(test_user2.posts)
    # print(sa.select(User.posts))



if __name__ == "__main__":
    main()
