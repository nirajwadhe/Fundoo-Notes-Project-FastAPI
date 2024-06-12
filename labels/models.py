from typing import List
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, create_engine , Boolean, BigInteger,DateTime
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from core.setting import settings

engine = create_engine(url = settings.DB_URL_NOTES)

session = sessionmaker(bind = engine, autoflush = False, autocommit = False)

def get_db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass

class Notes(Base):
    __tablename__ = "labels"
    labels_id:Mapped[int] = mapped_column(BigInteger, autoincrement = True, index = True, primary_key = True)
    label_name:Mapped[str] = mapped_column(String(length = 250))
    user_id:Mapped[int] = mapped_column(BigInteger,nullable=False)