from sqlalchemy.orm import Session

from core.logger import get_logger
from db.models.basal_logs import BasalLog
from schemas.basal import BasalCreate

logger = get_logger(__name__)


class BasalService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_basal(self, payload: BasalCreate, user_id: int) -> BasalLog:
        basal = BasalLog(
            timestamp=payload.get_timestamp(),
            units=payload.units,
            insulin=payload.insulin,
            time=payload.time,
            notes=payload.notes,
            user_id=user_id,
        )
        try:
            self.db.add(basal)
            self.db.commit()
            self.db.refresh(basal)
            logger.info(
                f"Basal saved: {basal.units}u {basal.insulin} at {basal.timestamp}"
            )
            return basal
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to save basal: {e}")
            raise
