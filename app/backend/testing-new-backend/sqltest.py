from datetime import datetime, timezone
from typing import Optional
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

Base = orm.declarative_base()

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String())
    full_name: Mapped[Optional[str]]

    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        full_name_temp = self.full_name
        if not full_name_temp:
            full_name_temp = "unnamed"
        return f"<User username={self.username!r}, full_name={full_name_temp!r}>"


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    time: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post content={self.content!r} author={self.author.username!r}>"



def main():
    test_user1 = User(username="test_user", full_name="Test User")
    test_user2 = User(username="second_test_user")
    test_post1 = Post(content="This is a Test Post", author=test_user1)
    test_post2 = Post(content="This is another Test Post", author=test_user1)
    test_post3 = Post(content="This is the third Test Post", author=test_user2)

    print(test_user1)
    print(test_user2)
    print(test_post1)
    print(test_post2)
    print(test_post3, "\n")
    print(test_user1.posts)
    print(test_user2.posts)


if __name__ == "__main__":
    main()
