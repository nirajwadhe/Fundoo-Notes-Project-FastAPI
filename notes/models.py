from typing import List
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey,Table,Column
from sqlalchemy import String, Integer, create_engine , Boolean, BigInteger,DateTime
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker
from sqlalchemy.orm import Mapped,mapped_column,relationship
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

label_association=Table("label_association",Base.metadata,Column("notes_id", ForeignKey("notes.notes_id")),
    Column("labels_id", ForeignKey("labels.labels_id")))

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
    labels:Mapped[List["Labels"]]=relationship(
        secondary=label_association, back_populates="notes"
    )
    
class Labels(Base):
    __tablename__ = "labels"
    labels_id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, index=True, primary_key=True)
    label_name: Mapped[str] = mapped_column(String(length=250))
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    notes:Mapped[List[Notes]]=relationship(
        secondary=label_association, back_populates="labels"
    )

  