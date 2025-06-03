import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table_of_contents = soup.find("div",id = "toc")
    headings = table_of_contents.find_all('li')
    data = []
    for heading in headings:
        heading_text = heading.find("span", class_ ="toctext").text
        heading_number = heading.fing("span", class_ = "tocnumber").text
        data.append({
            'heading_number': heading_number,
            'heading_text' : heading_text
        })
        return data
    
def export_data(data, file_name):
    with open(file_name, "w", new_file ="") as file:
        writer = csv.DictWriter(file, fieldnames =['heading_number','heading_text'])
        writer.writeheader()
        writer.writerows(data)
        
def main():
    ulr_parse = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    file_name = "python1.csv"
    data = get_data(ulr_parse)
    export_data(data, file_name)

    print("Done")

if __name__ == '__main__':
    main()