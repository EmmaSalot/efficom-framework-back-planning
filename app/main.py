# Libs imports
from fastapi import FastAPI
from pydantic import BaseModel

#local imports
from routers.users import router as user_router

app = FastAPI()

class RootReturnObj(BaseModel):
    Hello: str

@app.get("/")
async def helloWorld() -> RootReturnObj:
    return {"Hello": "World"}


@app.get("/say-hello-john")
async def helloJohn():
    return "Hello John!"

app.include_router(user_router, tags=["Users"])

