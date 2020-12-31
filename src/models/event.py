from sqlalchemy import sql

from .base import db_


class Event(db_.Model):
    __tablename__ = "Event"

    query: sql.Select

    id = db_.Column(db_.BigInteger, primary_key=True, index=True)
    text = db_.Column(db_.String)
    link_img = db_.Column(db_.String(300))
    inline_text = db_.Column(db_.String)
    inline_btn_link = db_.Column(db_.String)

    def __str__(self):
        return f"<Event text={self.text}>"