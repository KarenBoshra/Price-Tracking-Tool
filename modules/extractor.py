import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
from modules.text_processing import text_from_html
import re
from modules.generative_model import generate_content

def extract_data(url):
    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options)
    
    try:
        driver.get(url)
        html_content = driver.page_source
        full_text = text_from_html(html_content) 
        time.sleep(3) 
        return full_text
    except Exception as e:
        print(f"Error scraping data: {e}")
        return ""
    finally:
        driver.quit()

def save_to_csv(data):
    product_name, product_price, currency = data[0].strip(), data[1].strip(), data[2].strip()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    product_price = ''.join(filter(str.isdigit, product_price))

    formatted_product_price = '{:,.0f}'.format(float(product_price))

    fieldnames = ['Product Name', 'Product Price', 'Currency', 'Date/Time']

    with open('Database/priceTracker.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow({'Product Name': product_name,
                         'Product Price': formatted_product_price,
                         'Currency': currency,
                         'Date/Time': date_time})

def process_extracted_data(extracted_data):
    cleaned_data = extracted_data.replace('"', '').replace(',', '')

    cleaned_data = cleaned_data.lstrip('>')

    match = re.search(r'(?<=product price as a number, and what is the currency\? please separate each answer with a \*\*\*)\d+', cleaned_data)
    if match:
        product_price = match.group()
        product_price = int(product_price.replace(',', ''))
    else:
        product_price = None

    save_to_csv(cleaned_data.split('***'))

    return {'data': cleaned_data, 'product_price': product_price}
