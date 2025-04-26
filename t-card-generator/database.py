import locale

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/ordid/Documents/master-poke/t-card-generator/tcard.db"
app.secret_key = b'GXa3Kjm4FWJuWtN05Qk8oA'

db = SQLAlchemy(model_class=Base, app=app)

locale.setlocale(locale.LC_ALL, 'fr_FR')
