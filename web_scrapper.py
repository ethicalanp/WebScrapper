import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

url = "paste url"
response = requests.get(url)
if response.status_code == 200:
    page_content = response.text
else:
    print("Failed to retrieve the web page")
    page_content = ""


soup = BeautifulSoup(page_content, 'html.parser')


def extract_titles(soup):
    data_listings = soup.find_all('div', class_='product_pod')
    titles = [data.find('h3').find('a').get('title') for data in data_listings]
    return titles


titles = extract_titles(soup)
print("Titles on the first page:")
for title in titles:
    print(title)


next_page = soup.find('li', class_='next')
while next_page:
    next_page_url = url + next_page.find('a')['href']
    response = requests.get(next_page_url)
    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(page_content, 'html.parser')
        titles = extract_titles(soup)
        print(f"Titles on page: {next_page_url}")
        for title in titles:
            print(title)
        next_page = soup.find('li', class_='next')
    else:
        print("Failed to retrieve the next page")
        break


options = ChromeOptions()
options.headless = True
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url)


page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')
titles = extract_titles(soup)
driver.quit()


with open('data_listings.csv', 'w', newline='') as csvfile:
    fieldnames = ['title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for title in titles:
        writer.writerow({'title': title})


df = pd.read_csv('data_listings.csv')
print(df)

