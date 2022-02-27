from fastapi import FastAPI
import auth.main


app = FastAPI()

app.include_router(auth.main.router)