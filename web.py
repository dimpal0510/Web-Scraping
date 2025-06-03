import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = 'https://books.toscrape.com/'
PAGES_TO_SCRAPE = 3 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


all_books_data = []

print(f"Starting scraping for {PAGES_TO_SCRAPE} pages...")

for page_num in range(1, PAGES_TO_SCRAPE + 1):
    url = BASE_URL.format(page_num)
    print(f"Scraping page: {url}")

    try:
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        response.raise_for_status()

        
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('article', class_='product_pod')

        if not books:
            print(f"No books found on page {page_num}. Stopping.")
            break

        for book in books:
            
            title_tag = book.h3.a
            title = title_tag['title'] if title_tag else 'N/A'

            
            price_tag = book.find('p', class_='price_color')
            price = price_tag.text.strip() if price_tag else 'N/A'

           
            all_books_data.append({'Title': title, 'Price': price})

        print(f"Successfully scraped {len(books)} books from page {page_num}.")

     
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}")
       
    except Exception as e:
        print(f"An unexpected error occurred while processing page {page_num}: {e}")


print(f"\nScraping finished. Total books extracted: {len(all_books_data)}")


if all_books_data:
   
    csv_filename = 'scraped_books.csv'
    
    csv_headers = ['Title', 'Price']

    print(f"\nWriting data to {csv_filename}...")

    try:
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)

        
            writer.writeheader()

          
            for book_data in all_books_data:
                writer.writerow(book_data)

        print(f"Successfully wrote {len(all_books_data)} rows to {csv_filename}")
    except IOError as e:
        print(f"I/O error writing to CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing CSV: {e}")
else:
    print("\nNo data was scraped, so no CSV file will be generated.")

print("\nProgram finished.")