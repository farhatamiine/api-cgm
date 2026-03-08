from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from db.database import Base


class BasalLog(Base):
    __tablename__ = "basal_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    units = Column(Float(4), nullable=False)
    insulin = Column(String, nullable=True)  # "Glargine/Degludec/Tresiba"
    time = Column(String, nullable=True)  # "Night/Morning"
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
