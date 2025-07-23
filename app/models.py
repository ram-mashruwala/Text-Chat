from typing import List
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as orm
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

class Chats(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    users: Mapped[List[User]] = relationship(secondary=association_table, back_populates="chat")
    messages: Mapped[List["Messages"]] = relationship(back_populates="chat")

class Messages(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    chat: Mapped[Chats] = relationship(back_populates="messages")
