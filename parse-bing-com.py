import csv
import requests
from bs4 import BeautifulSoup


# Function to read data from the input CSV file and return it as a list of tuples
def read_input_csv(input_csv_file_path):
    data_read_csv = []
    with open(input_csv_file_path, mode='r') as file:
        csv_file = csv.reader(file)
        data_read_csv.extend((lines[0], lines[1]) for lines in csv_file)
    return data_read_csv


# Function to fetch data from the web and return it as a list of results
def fetch_data(data_getting_csv_file):
    storing_scrap_data = []
    rank = 1
    search_engine = "bing"
    previous_domain_catalog = None  # To keep track of the previous domain and catalog

    for domain_name, catalog_number in data_getting_csv_file:
        if (domain_name, catalog_number) != previous_domain_catalog:
            rank = 1  # Reset rank to 1 for a new domain and catalog
            previous_domain_catalog = (domain_name, catalog_number)

        url = f'https://www.bing.com/search?q={domain_name}+{catalog_number}'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('ol#b_results > li > h2 > a') or soup.select('ol#b_results > li > div > h2 > a')
        description = soup.select('ol#b_results > li > div > p') or soup.select('ol#b_results > li > div > div > p')
        title = soup.select('ol#b_results > li > h2 > a') or soup.select('ol#b_results > li > div > h2 > a')
        is_sponsored = bool(soup.select('div.scs_child_rpr.rpr_light'))

        for links_href, descriptions_text, title_text in zip(links, description, title):
            link_href = links_href['href']
            description_text = descriptions_text.get_text()
            title_text = title_text.get_text()

            result = [
                search_engine,
                domain_name,
                catalog_number,
                title_text,
                description_text,
                link_href,
                rank,
                is_sponsored,
            ]
            storing_scrap_data.append(result)
            rank += 1

    return storing_scrap_data


# Function to write the results to a CSV file
def write_to_csv(data_getting, output_csv_file_path):
    with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        csv_writer.writerow(
            ['SEARCH_ENGINE', 'DOMAIN', 'CATALOG_NUMBER', 'TITLE', 'DESCRIPTION', 'URL', 'RANK', 'IS_SPONSORED'])
        csv_writer.writerows(data_getting)


if __name__ == "__main__":
    input_file_path = 'input_files/input.csv'
    output_csv_path = 'output_data_bing.csv'

    # Read input data from the CSV file
    data = read_input_csv(input_file_path)

    # Fetch data from the web
    results = fetch_data(data)

    # Write the results to the output CSV file
    write_to_csv(results, output_csv_path)
