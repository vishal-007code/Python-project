import csv
import requests
from bs4 import BeautifulSoup

# Function to scrape product details from a single page
def scrape_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    scraped_data = []

    for product in products:
        product_url_elem = product.find('a', class_='a-link-normal s-no-outline')
        product_url = 'https://www.amazon.in' + product_url_elem['href'] if product_url_elem else 'N/A'
        
        product_name_elem = product.find('span', class_='a-size-medium a-color-base a-text-normal')
        product_name = product_name_elem.text.strip() if product_name_elem else 'N/A'

        product_price_elem = product.find('span', class_='a-offscreen')
        product_price = product_price_elem.text.strip() if product_price_elem else 'N/A'

        rating_elem = product.find('span', class_='a-icon-alt')
        rating = rating_elem.text.strip() if rating_elem else 'N/A'

        num_reviews_elem = product.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        num_reviews = num_reviews_elem.text.strip() if num_reviews_elem else 'N/A'

        additional_data = scrape_product_page(product_url)

        data = {
            'Product URL': product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': rating,
            'Number of Reviews': num_reviews,
            'Description': additional_data.get('Description', 'N/A'),
            'ASIN': additional_data.get('ASIN', 'N/A'),
            'Product Description': additional_data.get('Product Description', 'N/A'),
            'Manufacturer': additional_data.get('Manufacturer', 'N/A')
        }
        scraped_data.append(data)

    return scraped_data


# Function to scrape additional information from a product URL
def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    description_elem = soup.find('div', id='productDescription')
    description = description_elem.text.strip() if description_elem else 'N/A'

    asin_elem = soup.find('th', string='ASIN')
    asin = asin_elem.find_next('td').text.strip() if asin_elem else 'N/A'

    product_description_elem = soup.find('div', {'id': 'productDescription'})
    product_description = product_description_elem.text.strip() if product_description_elem else 'N/A'

    manufacturer_elem = soup.find('a', {'id': 'bylineInfo'})
    manufacturer = manufacturer_elem.text.strip() if manufacturer_elem else 'N/A'

    additional_data = {
        'Description': description,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }

    return additional_data

    
# Main scraping function
def scrape_amazon_products():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    num_pages = 20
    all_data = []

    for page in range(1, num_pages + 1):
        url = base_url + str(page)
        print(f"Scraping page {page}...")
        page_data = scrape_page(url)
        all_data.extend(page_data)

    # Save the scraped data to a CSV file
    filename = 'amazon_products.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames =['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)

    print("Scraping completed!")

# Call the main scraping function
scrape_amazon_products()
