from sqlalchemy.orm import Session

from core.logger import get_logger
from db.models.bolus_log import BolusLog
from schemas.bolus import BolusCreate
from services.glucose_service import GlucoseService

logger = get_logger(__name__)


class BolusService:
    def __init__(self, db: Session, glucose_service: GlucoseService) -> None:
        self.db = db
        self.glucose_service = glucose_service

    def create_bolus(self, payload: BolusCreate, user_id: int) -> BolusLog:
        """Persist a bolus event to the database."""

        if payload.glucose_at_injection is None:
            try:
                glucose = self.glucose_service.get_current()["sgv"]
            except Exception:
                glucose = None
        else:
            glucose = payload.glucose_at_injection

        bolus = BolusLog(
            timestamp=payload.get_timestamp(),
            units=payload.units,
            bolus_type=payload.bolus_type,
            meal_type=payload.meal_type,
            glucose_at_injection=glucose,
            inject_to_meal_min=payload.inject_to_meal_min,
            notes=payload.notes,
            user_id=user_id,
        )
        try:
            self.db.add(bolus)
            self.db.commit()
            self.db.refresh(bolus)
            logger.info(
                f"Bolus saved: {bolus.units}u {bolus.bolus_type} at {bolus.timestamp}"
            )
            return bolus
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to save bolus: {e}")
            raise
