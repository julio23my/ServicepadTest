## Start project
create a .env file inside this folder and add the following enviroments variables.


    DEBUG=True
    FLASK_ENV=development
    FLASK_APP=blogapi
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DATABASE_URL=sqlite:///database.db
    PASSWORD_KEY=3998d574f40b4521b44b7589f49384b0
    ALGORITHM=HS256

This is a example please don't use the same key that was expose

Now you just have to create the database

first you just have to execute python in this folder and after that you need to execute the following sentences

    import os
    from blogapi import db
    from blogapi.extensions import db
    from blogapi import create_app
    from blogapi.models import *
    from blogapi.extensions import load
    db.create_all(app=create_app())


After you just need to execute the following command in this folder
    
    flask run