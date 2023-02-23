import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


URL = 'https://www.dilovamova.com/index.php?page=142&calendar=fun-holidays'

def random_holiday():
    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')
    holiday = soup.find('div', class_='lCG')
    print(holiday.text)
    today = datetime.now().date().day
    if today == int(holiday.text.split(' ')[0]):
        return ('<b>Вітаю!</b> Сьогодні '+holiday.text)
    else:
        return('Нажаль сьогодні ніякого свята немає')


if __name__ == "__main__":
    random_holiday()