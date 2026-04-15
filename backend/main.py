from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database_postgres import engine, Base
from .routers import books, cantos, chapters, verses, content

app = FastAPI(title="Spiritual Scripture CMS API")

# Setup CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(cantos.router)
app.include_router(chapters.router)
app.include_router(verses.router)
app.include_router(content.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Spiritual Scripture CMS API"}
