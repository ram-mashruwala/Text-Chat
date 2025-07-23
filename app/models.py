from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Optional
from app import db
from sqlalchemy import Column, ForeignKey, Table, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

association_table = Table(
    "user_chats", db.metadata, 
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    chats: Mapped[Optional[List["Chats"]]] = relationship(secondary=association_table, back_populates="users")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password=password)

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} email={self.email}>"

class Chats(db.Model):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    users: Mapped[List[User]] = relationship(secondary=association_table, back_populates="chats")
    messages: Mapped[Optional[List["Messages"]]] = relationship(back_populates="chat", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Chats id={self.id}>"

class Messages(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    chat: Mapped[Chats] = relationship(back_populates="messages")
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    text: Mapped[str] = mapped_column(ForeignKey("user.id"))
    author_id: Mapped[int]

    author: Mapped[User] = relationship()

    def __repr__(self) -> str:
        return f"<Messages id={self.id} timestamp={self.timestamp} text={self.text} author-username={self.author.username}>"

