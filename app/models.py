from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime
from app.database import Base


class SoftwareDetails(Base):
    __tablename__ = "software_purchase"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    user = Column(String, nullable=False)
    department = Column(String, nullable=False)
    software = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

