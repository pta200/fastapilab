from fastapi import APIRouter, Depends, HTTPException
from ..core import crud, schemas
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db
import logging

logger = logging.getLogger(__name__)

user_router = APIRouter(
    prefix="/users",
    tags=["items"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@user_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("create new user....")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@user_router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: UUID, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


