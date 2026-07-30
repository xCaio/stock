from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supplies_routes import supplies_router
from auth_routes import auth_router
from movements_routes import movements_router
from dashboard_routes import dashboard_router
from users_routes import users_router

app = FastAPI()

app.include_router(supplies_router)
app.include_router(auth_router)
app.include_router(movements_router)
app.include_router(dashboard_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://SEU-FRONTEND.vercel.app",  # URL do front em prod 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)