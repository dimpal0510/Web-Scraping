import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_csv(url,csv_filename="scraped_links.csv"):
    
    print(f"Attempting to scrape: {url}")
    try:
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  
        html_content = response.text
        print("Successfully fetched HTML content.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    
    soup = BeautifulSoup(html_content, 'html.parser')

    
    links = soup.find_all('a')

    extracted_data = []
    if not links:
        print("No links found on the page.")
        return

    
    for index, link in enumerate(links):
        href = link.get('href') 
        text = link.get_text(strip=True) 

        if href:
            if href.startswith('/'):
                
                from urllib.parse import urljoin
                href = urljoin(url, href)
            elif not (href.startswith('http://') or href.startswith('https://')):
                
                if ':' in href: 
                    continue 
                else: 
                    from urllib.parse import urljoin
                    href = urljoin(url, href)


        extracted_data.append({
            'ID': index + 1,
            'URL': href if href else '', 
            'Link Text': text
        })

   
    csv_headers = ['ID', 'URL', 'Link Text']

    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)

            writer.writeheader() 
            writer.writerows(extracted_data) 
        print(f"Successfully scraped {len(extracted_data)} links and saved to '{csv_filename}'")
        print(f"The CSV file is located at: {os.path.abspath(csv_filename)}")
    except IOError as e:
        print(f"Error writing CSV file: {e}")


if __name__ == "__main__":
    
    target_url = "https://www.tops-int.com//" 

    scrape_csv(target_url, "tops1.csv")

    