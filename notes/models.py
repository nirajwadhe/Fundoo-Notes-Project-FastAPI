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
    __tablename__ = "notes"
    notes_id:Mapped[int] = mapped_column(BigInteger, autoincrement = True, index = True, primary_key = True)
    description:Mapped[str] = mapped_column(String(length = 1000))
    title:Mapped[str] = mapped_column(String(length=250))
    color:Mapped[str] = mapped_column(String(length=50))
    remainder:Mapped[Optional[datetime]] = mapped_column(DateTime)
    is_archive:Mapped[bool] = mapped_column(default=False)
    is_trash_bool:Mapped[bool] = mapped_column(default=False)
    user_id:Mapped[int] = mapped_column(BigInteger,nullable=False)

  