from .core.database import SessionLocal
from fastapi import HTTPException

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        HTTPException(status_code=400, detail="Request failed. Rolling back transaction")
    finally:
        db.close()