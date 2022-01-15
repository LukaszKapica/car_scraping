import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///oferty.db'

db = SQLAlchemy(app)
from models import Offers

alembic = Alembic()
alembic.init_app(app)


URL = 'https://www.otomoto.pl/osobowe/skoda/fabia'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(class_='optimus-app-njzfp e19uumca12')
# print(results.prettify())

samochody = []
car_elements = results.find_all("article", class_="optimus-app-1erv7ru e1b25f6f18")
for car_element in car_elements:
    car_dict ={}
    car_dict['price'] = car_element.find('span', class_="optimus-app-epvm6 e1b25f6f8").text
    rest_elements = car_element.find_all('li')
    # print(rest_elements)
    links = car_element.find_all('a')
    for link in links:
        link_url = link['href']
        # print(link_url)
        if 'oferta' in link_url:
            car_dict['link'] = link_url
    if rest_elements[0].text=='Niski przebieg':
        car_dict['year'] = int(rest_elements[1].text)
        car_dict['mileage'] = rest_elements[2].text
        car_dict['engine_size'] = rest_elements[3].text
        # print(rest_elements[2].text)
    else:
        car_dict['year'] = int(rest_elements[0].text)
        car_dict['mileage'] = rest_elements[1].text
        car_dict['engine_size'] = rest_elements[2].text
        # print(rest_elements[1].text)
    samochody.append(car_dict)
    # print(price_element.text.strip())
    # print(rest_elements[1].text)

# other_car_elements = results.find_all('article', class_="optimus-app-5vxqem e1b25f6f18")
# for car_element in other_car_elements:
#     price_element = car_element.find('span', class_="optimus-app-epvm6 e1b25f6f8")
#     print(price_element.text.strip())

# print(samochody)
# print(samochody[1]['price'])
import re
# print(re.sub('[^0-9]','',samochody[1]['price']))
for oferta in samochody:
    oferta['price'] = re.sub('[^0-9]','',oferta['price'])
    oferta['mileage'] = re.sub('[^0-9]','',oferta['mileage'])
    oferta['engine_size'] = re.sub('[^0-9]','',oferta['engine_size'])
    oferta['engine_size'] = oferta['engine_size'][0:-1]


# print(samochody)

interesting_offers = []
for element in samochody:
    if int(element['price'])<50000 and int(element['price'])>20000:
        interesting_offers.append(element)
print(interesting_offers)


# for element in samochody:
#     oferta = Offers(price=element['price'], link=element['link'], year=element['year'], mileage=element['mileage'],
#                     engine_size=element['engine_size'])
#     db.session.add(oferta)
#     db.session.commit()


@app.route('/')
def homepage():
    oferty = db.session.query(Offers.id, Offers.price, Offers.year, Offers.mileage, Offers.engine_size, Offers.link).all()
    header = ['ID', 'price', 'year', 'mileage', 'engine_size', "link"]
    return render_template('offers.html', header=header, oferty=oferty)

# flask login
# dodać użtkownikow
# flask app scheduler
# uzytkownik moze wybierać parametry na stronie i dostawać maile