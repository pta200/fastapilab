from fastapi import FastAPI
from .core.database import engine
from .core import models
from .apis import users, items

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.user_router)
app.include_router(items.item_router)




