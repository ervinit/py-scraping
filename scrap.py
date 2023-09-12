import requests
import random
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

proxy_address_list = [
    "101.98.83.161:8080",
    "103.247.152.125:3128",
    "180.189.196.167:8080",
    "103.156.193.97:8085",
    "103.76.164.50:3128",
    "103.240.187.36:8080",
    "103.5.109.253:8085",
    "103.156.192.253:8085",
    "101.100.148.136:80",
    "119.224.79.120:9812",
    "103.197.60.170:3128",
    "125.239.193.183:8080",
    "222.153.153.80:8080",
    "103.156.192.253:8090",
    "122.58.118.224:8080",
    "47.72.90.130:80",
    "222.153.121.26:8080"
]

proxy_address_list_us = [
    "191.101.1.116:80",
    "167.99.124.118:80",
    "73.85.129.115:80",
    "83.136.219.140:80",
    "147.182.132.21:80",
    "31.222.200.205:80",
    "141.148.63.29:80",
    "142.11.232.45:80",
    "138.68.225.200:80",
    "198.211.117.231:80",
    "207.2.120.58:80",
    "68.183.135.221:8082",
    "47.88.62.42:80"
]

def set_proxy(proxy_address):
    print(proxy_address)
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy_address}')

    return webdriver.Chrome(options=chrome_options)

def get_random_proxy():
    return random.choice(proxy_address_list_us)

page_num = 1
url = "https://www.trademe.co.nz/stores/Bivouac-Outdoor?sort_order=expiry_asc&page="
contain_product = True

file_path = 'data.csv'

while(contain_product):
    proxy_address = get_random_proxy()
    try:
        driver = set_proxy(proxy_address)
    
        req_url = url + str(page_num) + "&rptpath="
        response = requests.get(req_url)
        soup = BeautifulSoup(response.content, "html.parser")
        div_no_product = soup.find("div", id="customMessage")
        if div_no_product:
            contain_product = False
            driver.quit()
            break
        
        div_elements = soup.find_all("div", class_="supergrid-bucket")
        for div_element in div_elements:
            a_tags = div_element.find_all('a')
            for a_tag in a_tags:
                href = a_tag.get('href')
                element_info = a_tag.find("div", class_="info")
                element_title = a_tag.find("div", class_="title")
                element_price = a_tag.find("div", class_="listingBuyNowPrice")
                element_id = a_tag.find("div", class_="supergrid-listing")
                product_id = element_id.get("data-listingid")

                product_url = "https://www.trademe.co.nz" + href
                driver.get(product_url)
                # Extract the HTML content after the JavaScript has executed
                html = driver.page_source

                # Create a BeautifulSoup object to parse the HTML content
                soup = BeautifulSoup(html, 'html.parser')
                product_detail = soup.find("div", class_="tm-marketplace-listing__share-listing-container")

                page_view = '0'
                if product_detail:
                    views = product_detail.find("b")
                    if views:
                        page_view = views.text

                existing_data = []
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    existing_data = list(reader)

                with open(file_path, 'w', newline='') as file:
                    name = element_title.text.strip()
                    price = element_price.text.strip()
                    writer = csv.writer(file)

                    # Write the data to the CSV file
                    data = [product_id, name, product_url, price, page_view]
                    existing_data.append(data)
                    print(str(data))
                    writer.writerows(existing_data)

        page_num += 1
        print("===================== "+ str(page_num) +" ===================/n")
        time.sleep(1)
    except Exception as e:
        print("Error occurred:", e)
        time.sleep(1)