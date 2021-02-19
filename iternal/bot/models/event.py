from sqlalchemy import sql

from .base import db_


class Event(db_.Model):
    __tablename__ = "Event"

    query: sql.Select

    id = db_.Column(db_.Integer, primary_key=True, index=True, unique=True)
    text = db_.Column(db_.String)
    link_img = db_.Column(db_.String(300))
    inline_text = db_.Column(db_.String)
    inline_btn_link = db_.Column(db_.String(300))

    def __str__(self):
        return self.text
