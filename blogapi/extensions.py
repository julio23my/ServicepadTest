from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


load = load_dotenv()
db = SQLAlchemy()
migrate = Migrate()