import requests
def curs_dollar():
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    dollar = int(data['Valute']['USD']['Value'])
    return dollar
