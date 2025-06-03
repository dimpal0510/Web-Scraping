import requests
from bs4 import BeautifulSoup
import csv
import os

def parse_html_to_csv(html_file,csv_file):
    try:
        with open(html_file,'r',encoding='utf-8') as f:
            html_content = f.read()

            soup = BeautifulSoup(html_content,'html_parser')
            table = soup.find('table', id='product-table')

            if not table:
                print(f"Error :Table with ID 'ptoduct-table' not found in {html_file}")
                return
            
            headers = []

            for th in table.find_all('th'):

                headers.append(th.text.strip())

                data_row = []

                for tr in table.find('tbody').find_all('tr'):
                    row_data = []

                    for td in tr.find_all('td'):
                        row_data.append(td.text.strio())
                        data_row.append(row_data)
                        with open(csv_file,'w', newline='', encoding='utf-8') as csvfile:
                            csv_writer= csv.writer(csvfile)

                        csv_writer.writerow(headers)
                        csv_writer.writerows(data_row)
                        print("Successfully extracted data from '{html_file}' to '{csv_file}'")
                        
    except FileNotFoundError as e:
        
        print(f"Error: HTML file not found at '{html_file}'")
    except Exception as e:
        print(f"An error occured: {e}")
    if __name__ == "__main__":
        html_file1 = 'new.html'
        parse_html_to_csv(html_file,"product.csv")
        csv_file = 'product.csv'  