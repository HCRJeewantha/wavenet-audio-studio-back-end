from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from database.sqlite_connection import engine
from models.sqlite_models import Base

origins = ["*", "http://localhost:4200/"]

tags_metadata = [
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="Wave-Net Audio Studio",
    terms_of_service="",
    debug=True,
    responses={404: {"message": "Not Found"}},
    docs_url='/docs',
    version="1.0.1",
    redoc_url=None,
    contact={
        "name": "Ravindu Jeewantha",
        "email": "rjcolambage@gmail.com",
    },
    openapi_url='/apidocs.json'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the tables
Base.metadata.create_all(bind=engine)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1',
                port=8000, workers=1, reload=False)
