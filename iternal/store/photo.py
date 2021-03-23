from sqlalchemy.sql import expression

from .base import db_, TimedBaseModel


class Photo(TimedBaseModel):
    __tablename__ = "photos"

    title = db_.Column(db_.String(125))
    description = db_.Column(db_.String)
    author_id = db_.Column(db_.Integer, db_.ForeignKey("users.id", ondelete='CASCADE'))
    tags = db_.ForeignKey('tags', ondelete='NO ACTION')
    watches = db_.Column(db_.Integer)
    likes = db_.Column(db_.Integer)
    path = db_.Column(db_.String(255))
    is_private = db_.Column(db_.Boolean(), server_default=expression.false())
