from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.supplies import router as supplies_router
from app.routers.auth import router as auth_router
from app.routers.movements import router as movements_router
from app.routers.dashboard import router as dashboard_router
from app.routers.users import router as users_router

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
        "https://stock-frontend-dun-eight.vercel.app",
        "https://workflow.cabtec.com.br",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)