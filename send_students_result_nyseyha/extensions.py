from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db: SQLAlchemy = SQLAlchemy()
mail: Mail = Mail()