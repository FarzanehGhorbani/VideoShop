'''This package contains  modules for authentication.

auth/
    __init__.py
    crud.py : contains function for create user and update user and search user.

    models.py : models for signup and login that will be used in database and inherit from BaseModel.

    publisher.py : publish message to email queue.

    main.py : contains /auth/signup and auth/signup/verified/token and /auth/login.

    db_mongodb.py : contains database connection and mongodb models.

    jwt_handler.py : contains jwt token handler for generate and verify token.
    
'''
