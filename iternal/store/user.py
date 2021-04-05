from .base import db_, TimedBaseModel


class User(TimedBaseModel):
    """
    User need for store User model,
    uses for indentifi
    """
    __tablename__ = 'users'

    user_id = db_.Column(db_.BigInteger)
    username = db_.Column(db_.String(50))
    full_name = db_.Column(db_.String(100))
    login = db_.Column(db_.String(100))
    email = db_.Column(db_.String(200))
    password = db_.Column(db_.String(255))  # there must be hash
    referral = db_.Column(db_.Integer)
    description = db_.Column(db_.String)
    is_admin = db_.Column(db_.Boolean, default=True)
