from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from db.database import Base


class BolusLog(Base):
    __tablename__ = "bolus_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    units = Column(Float(2), nullable=False)
    meal_type = Column(String, nullable=True)  # low_gi/medium_gi/high_gi
    glucose_at_injection = Column(Float(2), nullable=True)
    bolus_type = Column(String(50), default="manual", nullable=False)
    inject_to_meal_min = Column(Integer, nullable=True)  # how many min before eating
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
