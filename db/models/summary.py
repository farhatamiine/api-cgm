from typing import Optional

from sqlalchemy import Column, Date, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class DailySummary(Base):
    __tablename__ = "daily_summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True)
    tir = Column(Float(4), nullable=True)
    tar = Column(Float(4), nullable=True)
    tbr = Column(Float(4), nullable=True)
    mean = Column(Float(4), nullable=True)
    gmi = Column(Float(4), nullable=True)
    cv = Column(Float(4), nullable=True)
    hypo_count = Column(Integer, nullable=True)
    hypo_min = Column(Integer, nullable=True)
    worst_meal = Column(String, nullable=True)
    best_meal = Column(String, nullable=True)
    ai_insight: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
