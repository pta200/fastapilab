from fastapi import APIRouter, Depends, HTTPException
from core import crud
from core import schemas
from sqlalchemy.orm import Session
from uuid import UUID
from ..dependencies import get_db

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
