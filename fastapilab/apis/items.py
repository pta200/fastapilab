from fastapi import APIRouter, Depends, HTTPException
from ..core import crud, schemas
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db
import logging

logger = logging.getLogger(__name__)

item_router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@item_router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@item_router.post("/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: UUID, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    logger.info("add new item....")
    return crud.create_user_item(db=db, item=item, user_id=user_id)