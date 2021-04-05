from .base import db_, TimedBaseModel


class Event(TimedBaseModel):
    """
    Uses for create Event
    """
    __tablename__ = "event"

    text = db_.Column(db_.String)
    link_img = db_.Column(db_.String(300))
    inline_text = db_.Column(db_.String)
    inline_btn_link = db_.Column(db_.String(300))
