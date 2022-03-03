# from fastapi import FastAPI,Request
# import auth.main

# import profile.main

# # HOST_URL='http://192.168.63.60:8000'

# app = FastAPI()



# app.include_router(auth.main.router)
# app.include_router(profile.main.router)

from profile import create_app

app = create_app()

