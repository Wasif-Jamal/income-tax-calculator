from fastapi import FastAPI
from app.routes.tax import router as tax_router
from app.db.database import Base, engine

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# include routes
app.include_router(tax_router)