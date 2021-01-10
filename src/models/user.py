from sqlalchemy import sql

from .base import db_


class User(db_.Model):
    __tablename__ = 'users'

    id = db_.Column(db_.Integer, primary_key=True, index=True, unique=True)
    user_id = db_.Column(db_.BigInteger)
    username = db_.Column(db_.String(50))
    full_name = db_.Column(db_.String(100))
    login = db_.Column(db_.String(100))
    email = db_.Column(db_.String(200))
    password = db_.Column(db_.String(200))  # there must be hash
    referral = db_.Column(db_.Integer)
    description = db_.Column(db_.String)
    is_admin = db_.Column(db_.Boolean)

    query: sql.Select

    def __str__(self):
        return f"<User(id='{self.id}', fullname='{self.full_name}', username='{self.username}')>"
