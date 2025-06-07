from app.database import Base
from sqlalchemy import Column, String, Integer, Date


class PostModel(Base):
    __tablename__ = "post_db"

    id = Column(Integer, primary_key=True, index=True)
    header = Column(String, unique=True)
    text = Column(String)
    created_at = Column(Date)
