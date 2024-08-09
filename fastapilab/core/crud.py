from uuid import UUID
from sqlalchemy.orm import Session, class_mapper
from sqlalchemy import types
import re
from . import models
from . import schemas


def get_field_type(column, val):
    if type(column.type) is types.DateTime:
        return datetime.strptime(val, "%Y-%m-%dT%H:%M:%SZ")
    
    if type(column.type) is types.Integer:
        return int(val)
    
    return val

def generate_filter(column, v):
    if re.match(r"^!", v):
        """__ne__"""
        val = re.sub(r"!", "", v)
        return column.__ne__(get_stat_type(column, val))

    if re.match(r">(?!=)", v):
        """__gt__"""
        val = re.sub(r">(?!=)", "", v)
        logger.debug("match gt %s", val)
        return column.__gt__(get_stat_type(column, val))

    if re.match(r"<(?!=)", v):
        """__lt__"""
        val = re.sub(r"<(?!=)", "", v)
        logger.debug("match lt %s", val)
        return column.__lt__(get_stat_type(column, val))

    if re.match(r">=", v):
        """__ge__"""
        val = re.sub(r">=", "", v)
        return column.__ge__(get_stat_type(column, val))

    if re.match(r"<=", v):
        """__le__"""
        val = re.sub(r"<=", "", v)
        return column.__le__(get_stat_type(column, val))

    if re.match(r"(\w*),(\w*)", v):
        """between"""
        a, b = re.split(r",", v)
        return column.between((get_stat_type(column, a)), (get_stat_type(column, b)))

    """ default __eq__ """
    return column.__eq__(get_stat_type(column, v))

def build_query(table, filter_by):
    filters = []
    for k, v in filter_by.items():
      mapper = class_mapper(table)
      if not hasattr(mapper.columns, k):
        continue
      filters.append(generate_filter(mapper.columns[k], "{}".format(v))
    return filters

def get_filtered_user(db: Session, api_filters: dict):
    """
    Add operators to the value being filtered. Example
    ?foo=>1
    ?foo=<1
    ?foo=>=1 
    ?foo=<=1
    ?foo=!1
    ?foo=1 
    'between' opertor = ?foo=a,b
        filter_by = {
          "column1": "!1", # not equal to
          "column2": "1",   # equal to
          "column3": ">1",  # great to. etc...
        }
    """

    return db.query(models.User).filter(and_(*build_query(models.User, api_filters)).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, user_name=user.user_name)
    db.add(db_user)
    db.flush()
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: UUID):
    db_item = models.Item(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.flush()
    return db_item
