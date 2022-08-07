from fastapi import FastAPI
from .core.database import engine
from .core import models
from .apis import users, items
import logging
from sys import stdout

models.Base.metadata.create_all(bind=engine)

# Define logger
handler = logging.StreamHandler(stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # set logger level
logger.addHandler(handler)

app = FastAPI()
app.include_router(users.user_router)
app.include_router(items.item_router)




