from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate

load = load_dotenv()
db = SQLAlchemy()
migrate = Migrate()