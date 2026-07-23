from fastapi import FastAPI
from supplies_routes import supplies_router
from auth_routes import auth_router
app = FastAPI()

app.include_router(supplies_router)
app.include_router(auth_router)