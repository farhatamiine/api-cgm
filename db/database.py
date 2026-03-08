from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from core.config import get_settings





settings = get_settings()

engine = create_engine(url=settings.database_url)

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def check_connection():
    try:
        with engine.connect() as conn:
            print(f"✅ Database connected successfully {conn}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")