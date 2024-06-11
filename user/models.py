from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, create_engine , Boolean, BigInteger
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from core.setting import settings

# DB_URL =   "mysql+pymysql://root:Niraj1531@localhost:3306/fundoo_notes"

engine = create_engine(url = settings.DB_URL)

session = sessionmaker(bind = engine, autoflush = False, autocommit = False)

def get_db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id:Mapped[int] = mapped_column(BigInteger, autoincrement = True, index = True, primary_key = True)
    username:Mapped[str] = mapped_column(String(length = 50))
    password:Mapped[str] = mapped_column(String(length=250))
    first_name:Mapped[str] = mapped_column(String(length=50))
    last_name:Mapped[str] = mapped_column(String(length=50))
    email:Mapped[str] = mapped_column(String(length=100))
    is_verified:Mapped[bool] = mapped_column(default=False)
    
  