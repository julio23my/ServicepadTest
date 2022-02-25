## Start project
create a .env file inside this folder and add the following enviroments variables.


    DEBUG=True
    FLASK_ENV=development
    FLASK_APP=blogapi
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DATABASE_URL=sqlite:///database.db
    SECRET_KEY=3998d574f40b4521b44b7589f49384b0
    ALGORITHM=HS256
    DATABASE_URL=postgresql+psycopg2://test:password@localhost:5432/example

This is a example please don't use the same key that was expose

    
    docker-compose up


After you just need to execute this following commands in this folder
    
    flask db init
    flask db migrate
    flask db upgrade
    flask run
