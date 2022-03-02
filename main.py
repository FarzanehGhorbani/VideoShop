from fastapi import FastAPI,Request
import auth.main
# import profile.main

app = FastAPI()


app.include_router(auth.main.router)
# app.include_router(profile.main.router)
