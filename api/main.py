from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import auth, profile

description = """
Users API - a simple prototype using FastAPI, Docker, and MySQL. 🚀
This is inspired by Eric Roby's Udemy Course: https://www.udemy.com/course/fastapi-the-complete-course/

You will be able to:

* **Register for account**
* **Log in**
* **Edit your profile**
* **Log out**
"""

# Instantiate FastAPI to app variable

origins = ["*"]

app = FastAPI(
    title="Users API",
    description=description,
    summary="Users API - a prototype, built using FastAPI, Docker, MySQL",
    version="2.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Added middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate database
models.Base.metadata.create_all(bind=engine)

# If you want to add modules, add entry here.
app.include_router(auth.router)
app.include_router(profile.router)
