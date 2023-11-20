from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routes import router
from api.database import close, connect

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect()
    yield
    await close()
    

app = FastAPI(title="RPN Calculator API", lifespan=lifespan)
app.include_router(router)
