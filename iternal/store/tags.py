from .base import db_, BaseModel


class Tag(BaseModel):
    __tablename__ = "tags"

    name = db_.Column(db_.String(125))
    desc = db_.Column(db_.String)
    popularity = db_.Column(db_.Integer())
