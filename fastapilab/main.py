from fastapi import FastAPI
from core.database import engine
from core import models
from apis import users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users)




