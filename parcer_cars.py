import requests
from bs4 import BeautifulSoup
import csv


HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.117 Safari/537.36', 'accept': '*/*'}


def save_file(cars, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'price', 'year', 'mileage', 'engine',
                         'v_engine', 'power', 'gearbox', 'wheels',
                         'color', 'link'])
        for car in cars:
            writer.writerow([car['name'], car['price'], car['year'], car['mileage'],
                             car['engine'], car['v_engine'], car['power'],
                             car['gearbox'], car['wheels'], car['color'], car['link']])


# Выборка нужных параметров -----------------------
# Наименование

def get_name(car):
    name = car.find('h3').find('a').text
    return name


# -----------------------------------------------------
# Цена
def get_price(car):
    price = car.find('div', class_='ListingItemPrice-module__content')
    # print(type(price))
    if price is None:
        return None
    new = ''
    for char in price.text:
        if char.isdigit():
            new += char
    return int(new)


# -----------------------------------------------------
# Год выпуска
def get_year(car):
    year = car.find('div', class_='ListingItem-module__year')
    return int(year.text)


# -----------------------------------------------------
# Пробег
def get_mileage(car):
    mileage = car.find('div', class_='ListingItem-module__kmAge')
    new = ''
    for char in mileage.text:
        if char.isdigit():
            new += char
    return int(new)


# -----------------------------------------------------
# Двигатель
def get_engine(car):
    engine = car.find('div', class_='ListingItemTechSummaryDesktop__cell')
    if 'Дизель' in engine.text:
        return 'Дизель'
    else:
        return 'Бензин'


# -----------------------------------------------------
# Объем двигателя
def get_v_engine(car):
    v_engine = car.find('div', class_='ListingItemTechSummaryDesktop__cell')
    v = float(v_engine.text[:3])
    return v


# -----------------------------------------------------
# Мощность двигателя
def get_power(car):
    power = car.find('div', class_='ListingItemTechSummaryDesktop__cell')
    if power.text[8:-14].isdigit():
        return int(power.text[8:-14])
    else:
        return None


# -----------------------------------------------------
# Коробка передач
def get_gearbox(car):
    gearbox = car.find('div',
                       class_='ListingItemTechSummaryDesktop ListingItem-module__techSummary')
    gearbox_name = gearbox.findAll('div', class_='ListingItemTechSummaryDesktop__cell')[
        1]
    return gearbox_name.text


# -----------------------------------------------------
# Ведущие колеса
def get_wheels(car):
    wheels = car.find('div',
                      class_='ListingItemTechSummaryDesktop ListingItem-module__techSummary')
    wheels_name = wheels.findAll('div', class_='ListingItemTechSummaryDesktop__cell')[3]
    return wheels_name.text


# -----------------------------------------------------
# Цвет
def get_color(car):
    color = car.find('div',
                     class_='ListingItemTechSummaryDesktop ListingItem-module__techSummary')
    color_name = color.findAll('div', class_='ListingItemTechSummaryDesktop__cell')[4]
    return color_name.text


# -----------------------------------------------------
# Ссылка
def get_link(car):
    link = car.find('a').get('href')
    return link


def get_html(url, params=None):
    result = requests.get(url, headers=HEADERS, params=params)
    result.encoding = 'utf8'
    return result


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.findAll('div', {'class': 'ListingItem-module__container'})
    car_list = []
    for car in cars:
        car_list.append({
            'name': get_name(car),
            'price': get_price(car),
            'year': get_year(car),
            'mileage': get_mileage(car),
            'engine': get_engine(car),
            'v_engine': get_v_engine(car),
            'power': get_power(car),
            'gearbox': get_gearbox(car),
            'wheels': get_wheels(car),
            'color': get_color(car),
            'link': get_link(car)
        })
        # print(car, end='\n')
        # print(car.find('a', class_='ListingItemTitle-module__link').text)
        # print(car.find('div', class_='ListingItemPrice-module__content').text)
        # print(car_list[0])
    return car_list


def get_pages_count(html):
    soup = BeautifulSoup(html, 'lxml')
    pagination = False  
    try:
        panel = soup.find('span', class_='ListingPagination-module__pages')
        pagination = panel.findAll('span', class_='Button__text')
    except:
        pass

    if pagination:
        return int(pagination[-1].text)
    else:
        return 1


# def main(url):
#     print('Введите адрес с сайта auto.ru')
#     html = get_html(url)
#     if html.status_code == 200:
#         car_list = []
#         pages = get_pages_count(html.text)
#         for page in range(1, 3):
#             print(f'Парсинг страницы {page} из {pages} ...')
#             html = get_html(url, params={'page': page})
#             car_list.extend(get_data(html.text))
#         print('Парсинг завершен успешно!')
#         # print(car_list[0])
#         save_file(car_list, 'cars.csv')
#     else:
#         print('Error')


# if __name__ == '__main__':
#     main()
