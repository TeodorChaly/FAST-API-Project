import csv


async def get_links(path):
    with open(path, newline='', encoding='utf-16') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')

        url_list = []

        for row in reader:
            print(row['URL'])
            url_list.append(row['URL'])

        return url_list
