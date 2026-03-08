from sqlalchemy import Column, DateTime, Float, Integer, String

from db.database import Base


class HypoEvent(Base):
    __tablename__ = "hypo_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lowest_value = Column(Float(3), nullable=False)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    duration_min = Column(Integer, nullable=True)
    recovery_min = Column(Integer, nullable=True)
    treated_with = Column(String, nullable=True)  # "3 sugar cubes"
    notes = Column(String, nullable=True)
