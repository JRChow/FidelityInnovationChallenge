"""Web Scripting."""
from bs4 import BeautifulSoup
import requests
import re
import csv

weatherData = []
dayWeather = {}
url = "https://www.accuweather.com/en/hk/hong-kong/1123655/month/1123655?monyr=10/01/2017"
data = requests.get(url).text.encode('utf-8').decode('ascii', 'ignore')
soup = BeautifulSoup(data, "html.parser")
# print(soup.prettify().encode('utf-8'))
table = soup.find("table", {"class": "calendar calendar-block "})
# print(table.prettify().encode('utf-8'))
table_body = table.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    for col in cols:
        date = col.find('h3').text
        print(date)
        # date = str(col.find('time'))
        # print(date[6:10])
        spans = col.find_all('span')
        temp = []
        for span in spans:
            raw_day = re.sub("\D", "", span.text.encode('utf-8'))
            print(raw_day)
            temp.insert(len(temp), int(raw_day))
        dayWeather['date'] = date.encode('utf-8')
        dayWeather['high'] = temp[0]
        dayWeather['low'] = temp[1]
        weatherData.insert(len(weatherData), dayWeather.copy())
        print('------------------------------------------------------------')
print(weatherData)

keys = weatherData[0].keys()
with open('oct_weather.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(weatherData)
