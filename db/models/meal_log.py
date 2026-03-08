from db.database import Base

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String


class MealLog(Base):
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meal_type = Column(String, nullable=False)  # low_gi/medium_gi/high_gi
    carbs_g = Column(Float(3), nullable=True)
    description = Column(String, nullable=True)  # "oats + whey + coconut milk"
    glucose_before = Column(Float(3), nullable=True)
    glucose_peak = Column(Float(3), nullable=True)
    result = Column(String, nullable=True)  # spike/stable/low
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
