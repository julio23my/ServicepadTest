from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load = load_dotenv()
db = SQLAlchemy()