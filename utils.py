import csv


# Function to read data from an input CSV file
def read_input_csv(input_csv_file_path):
    data_read_csv = []
    with open(input_csv_file_path, mode='r') as file:
        csv_file = csv.reader(file)
        # Iterate through each row in the CSV file
        data_read_csv.extend((lines[0], lines[1]) for lines in csv_file)
    return data_read_csv


# Function to write data to an output CSV file
def write_to_csv(data_getting, output_csv_file_path):
    with open(output_csv_file_path, mode='w', newline='', encoding='utf-8') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        # Write a header row with column names to the output CSV file
        csv_writer.writerow(
            ['SEARCH_ENGINE', 'DOMAIN', 'CATALOG_NUMBER', 'TITLE', 'DESCRIPTION', 'URL', 'RANK', 'IS_SPONSORED'])
        # Write the data to the output CSV file
        csv_writer.writerows(data_getting)


# Function to store scraped data in a structured format
def store_scrap_data(links: object, description: object, title: object, search_engine: object, catalog_number: object,
                     domain_name: object, rank: object, is_sponsored: object) -> object:
    storing_scrap_data = []
    for links_href, descriptions_text, title_text in zip(links, description, title):
        link_href = links_href['href']
        description_text = descriptions_text.get_text().strip()
        title_text = title_text.get_text().strip()

        result = [
            search_engine,
            domain_name,
            catalog_number,
            title_text,
            description_text,
            link_href,
            rank,
            is_sponsored
        ]
        # Append the result to the storing_scrap_data list
        storing_scrap_data.append(result)
        rank += 1  # Increment the rank

    return storing_scrap_data
