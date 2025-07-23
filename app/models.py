from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from app import db
from sqlalchemy import Column, ForeignKey, Table, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

association_table = Table(
    "user_chats", db.metadata, 
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(index=True)
    chats: Mapped[List["Chats"]] = relationship(secondary=association_table, back_populates="users")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password=password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password=password)

class Chats(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    users: Mapped[List[User]] = relationship(secondary=association_table, back_populates="chat")
    messages: Mapped[List["Messages"]] = relationship(back_populates="chat")

class Messages(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    chat: Mapped[Chats] = relationship(back_populates="messages")
