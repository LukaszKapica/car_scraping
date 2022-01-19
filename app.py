import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from pobieranie_przetwarzanie import samochody

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///oferty.db'

db = SQLAlchemy(app)
from models import Offers

alembic = Alembic()
alembic.init_app(app)


# for element in samochody:
#     oferta = Offers(price=element['price'], link=element['link'], year=element['year'], mileage=element['mileage'],
#                     engine_size=element['engine_size'])
#     db.session.add(oferta)
#     db.session.commit()


@app.route('/index/', methods=['GET', 'POST'])
def index():
    oferty = db.session.query(Offers.id, Offers.price, Offers.year, Offers.mileage, Offers.engine_size, Offers.link).all()
    header = ['ID', 'price', 'year', 'mileage', 'engine_size', "link"]
    return render_template('offers.html', header=header, oferty=oferty)


select_list = []


@app.route('/select/', methods=['GET', "POST"])
def select():
    if request.method == 'POST':
        selector = list(request.form.values())
        select_list.append(selector)
        print(selector)
        return redirect('/')


@app.route('/')
def homepage():
    return render_template('filter.html')

# flask login
# dodać użtkownikow
# flask app scheduler
# uzytkownik moze wybierać parametry na stronie i dostawać maile
print(select_list)