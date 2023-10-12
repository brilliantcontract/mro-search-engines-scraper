import requests
from bs4 import BeautifulSoup
import csv
from utlis import read_input_csv

def extract_data_from_main_paths(main_paths, domain_name, catalog_number, results, rank,
                                 link_selector, description_selector, title_selector):
    search_engine = "YAHOO"
    for main_path in main_paths:
        # Extract links within the main path
        link_href = main_path.select_one(link_selector)
        link_href = link_href.get('href') if link_href else None

        # Extract description within the main path
        description_text = main_path.select_one(description_selector)
        description_text = description_text.get_text() if description_text else None

        # Extract title within the main path
        title_text = main_path.select_one(title_selector)
        title_text = title_text.get_text() if title_text else None
        is_sponsored = bool(main_path.select('div.compList.ad-ql.mt-0'))
        results.append(
            [search_engine, domain_name, catalog_number, title_text, description_text, link_href, rank, is_sponsored])

        # Increment rank for main_path_selector
        rank += 1

    return rank



def write_data_to_csv(output_csv_path, data):
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        csv_writer.writerow(
            ['SEARCH_ENGINE', 'DOMAIN', 'CATALOG_NUMBER', 'RANK', 'URL', 'TITLE', 'DESCRIPTION', 'IS_SPONSORED'])
        csv_writer.writerows(data)

def fetch_data_and_store_in_csv(input_file_path, output_csv_path):
    # Read data from CSV
    data = read_input_csv(input_file_path)

    # Initialize a list to store data for each result
    results = []

    # CSS selectors for the main paths
    main_path_selector = 'ol.scta.reg.searchCenterTopAds > li > div'
    main_path_selector2 = 'ol.reg.searchCenterMiddle > li > div'

    current_catalog_number = None
    rank_main_path_selector = 1

    for lines in data:
        domain_name = lines[0]
        catalog_number = lines[1]

        # Check if a new catalog number is encountered
        if catalog_number != current_catalog_number:
            rank_main_path_selector = 1  # Reset rank to 1 for the new catalog number
            current_catalog_number = catalog_number

        url = f'https://search.yahoo.com/search?p={domain_name}+{catalog_number}'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Process main_path_selector
        main_paths = soup.select(main_path_selector)
        rank_main_path_selector = extract_data_from_main_paths(main_paths, domain_name, catalog_number, results,
                                                               rank_main_path_selector,
                                                               link_selector='div > div > div > a',
                                                               description_selector='div > div > div > div > p',
                                                               title_selector='div > div > div > a > h3 > span')

        # Process main_path_selector2
        main_paths2 = soup.select(main_path_selector2)
        rank_main_path_selector2 = extract_data_from_main_paths(main_paths2, domain_name, catalog_number, results,
                                                                rank_main_path_selector + 1,
                                                                # Start from where the previous rank ended
                                                                link_selector='div.compTitle.options-toggle > h3 > a',
                                                                description_selector='div.compText.aAbs > p > span',
                                                                title_selector=' div > h3 > a > span')

    # Write results to a CSV file
    write_data_to_csv(output_csv_path, results)

if __name__ == "__main__":
    input_file_path = 'input_files/input.csv'
    output_csv_path = 'output_data_yahoo.csv'

    fetch_data_and_store_in_csv(input_file_path, output_csv_path)
