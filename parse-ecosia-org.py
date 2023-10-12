import requests
from bs4 import BeautifulSoup
from utlis import read_input_csv, write_to_csv, store_scrap_data


# Function to fetch data from the web and return it as a list of results
def fetch_data(data_getting_csv_file):
    result_after_getting_all_data = []
    rank = 1
    search_engine = "ECOSIA"
    previous_domain_catalog = None  # To keep track of the previous domain and catalog

    for domain_name, catalog_number in data_getting_csv_file:
        if (domain_name, catalog_number) != previous_domain_catalog:
            rank = 1  # Reset rank to 1 for a new domain and catalog
            previous_domain_catalog = (domain_name, catalog_number)

        url = f'https://www.ecosia.org/search?q={domain_name}+{catalog_number}'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('a.result__link.result__link.link.link--as-a.link--color-result')
        description = soup.select('p.web-result__description')
        title = soup.select('h2.result-title__heading')
        is_sponsored = False
        data_getting_after_scraping = store_scrap_data(links, description, title, search_engine, catalog_number,
                                                       domain_name, rank, is_sponsored)
        result_after_getting_all_data.extend(iter(data_getting_after_scraping))
    return result_after_getting_all_data


# Function to write the results to a CSV file

if __name__ == "__main__":
    input_file_path = 'input_files/input.csv'
    output_csv_path = 'output_data_ecosia.csv'

    # Read input data from the CSV file
    data = read_input_csv(input_file_path)

    # Fetch data from the web
    results = fetch_data(data)

    # Write the results to the output CSV file
    write_to_csv(results, output_csv_path)
