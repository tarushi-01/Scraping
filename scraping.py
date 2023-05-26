import requests
from bs4 import BeautifulSoup
import csv


def scrape_product_details(url: str):
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)

    description = soup.find('span', {'id': 'productTitle'}).text.strip()
    # print(description)

    product_description = ""
    product_description_list = soup.find('div', {'id': 'feature-bullets'}).find_all('span', {'class': 'a-list-item'})

    for item in product_description_list:
        description = item.text.strip()
        product_description += description + ":"

    # print(product_description)
    try:
        manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
    except:
        manufacturer = "Manufacturer not available"
    # print(manufacturer)

    return description, product_description, manufacturer


def scrape_amazon_pages(count: int):
    base_url = "https://www.amazon.in/s"

    for page in range(1, count + 1):
        params = {"k": "bags", "page": page}
        response = requests.get(base_url, headers=headers, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_listings = soup.find_all('div', {'data-component-type': 's-search-result'})
        for listing in product_listings:
            # print(listing)
            product_url = "https://www.amazon.in" + listing.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            print(product_url)
            product_name = listing.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
            print(product_name)
            product_price = listing.find('span', {'class': 'a-offscreen'}).text.strip()
            print(product_price)
            try:
                product_rating = listing.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            except AttributeError:
                product_rating = "No rating, sponsored product"
            print(product_rating)
            num_reviews = listing.find('span', {'class': 'a-size-base'}).text.strip()
            print(num_reviews)
            asin = listing.attrs['data-asin']
            print(asin)

            description, product_description, manufacturer = scrape_product_details(product_url)

            data2 = {
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': product_rating,
                'Number of Reviews': num_reviews,
                'Description': description,
                'ASIN': asin,
                'Product Description': product_description,
                'Manufacturer': manufacturer
            }

            # Write the data to csv file immediately after scraping the data for each product so not to
            # lose the data in case of any error
            write_csv(data2)


# Write the data to csv file without headers
def write_csv(data):
    csv_file = 'amazon_products_new.csv'
    fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
                  'Description', 'ASIN', 'Product Description', 'Manufacturer']
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)


# Create a CSV file with headers
def create_csv_file():
    csv_file = 'amazon_products_new.csv'
    fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
                  'Description', 'ASIN', 'Product Description', 'Manufacturer']
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'close'
}

# Specify the number of pages to scrape
num_pages = 20
create_csv_file()

# Scrape the data
scrape_amazon_pages(num_pages)

print("Data scraping completed")
