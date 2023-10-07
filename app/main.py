from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes import products, users, auth, favorites
from .config import settings


# models.Base.metadata.create_all(bind=engine)    
# command untuk sqlalchemy untuk membuat semua table pada saat pertama kali, sudah tidak dipakai karena pakai alembiq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#allow semua situs untuk mengakses api
    allow_credentials=True,    
    allow_methods=["*"],    
    allow_headers=["*"],
)

@app.get("/")
def root():
    return{"message":"hello world docker"}

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(favorites.router)
