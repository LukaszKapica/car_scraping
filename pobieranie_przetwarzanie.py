import requests
from bs4 import BeautifulSoup


URL = 'https://www.otomoto.pl/osobowe/skoda/fabia'
page = requests.get(URL)
# print(page.text)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(class_="ooa-p2z5vl e19uumca5")
# print(results.prettify())

samochody = []
car_elements = results.find_all("article", class_="ooa-1h8h0y4 e1b25f6f18")
for car_element in car_elements:
    car_dict ={}
    car_dict['price'] = car_element.find('span', class_="ooa-epvm6 e1b25f6f8").text
    rest_elements = car_element.find_all('li')
    # print(rest_elements)
    links = car_element.find_all('a')
    for link in links:
        link_url = link['href']
        if not link.text == 'Więcej' and not link.text == 'Więcej ogłoszeń tego dealera':
            car_name = link.text
            car_dict['name'] = car_name
        # print(car_name)
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


print(samochody)

interesting_offers = []
for element in samochody:
    if int(element['price'])<50000 and int(element['price'])>20000:
        interesting_offers.append(element)
# print(interesting_offers)