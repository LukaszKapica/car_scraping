from app import db


class Offers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    link = db.Column(db.String)
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    engine_size = db.Column(db.Integer)