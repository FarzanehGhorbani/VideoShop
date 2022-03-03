from fastapi import FastAPI,Request
from passlib.context import CryptContext
from .core.db import Mongo
from .core.security import JWT,MyMiddleware

jwt_manager: JWT = JWT(secret="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithm="HS256")
bcrypt = CryptContext(schemes=["bcrypt"])


def create_app(config: dict = None) -> FastAPI:
    app = FastAPI()
    

    from .api import router
    
    @app.on_event("startup")
    async def startup():
        await Mongo.create_connection()

        
    app.include_router(router)
    my_middleware = MyMiddleware()  # Do whatever you need the class for here
    app.middleware("http")(my_middleware)
    
    return app
