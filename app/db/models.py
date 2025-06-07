from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    kilometers = Column(Numeric(10, 2), nullable=False)
    miles = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False,  server_default=func.now()) 