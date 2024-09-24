import csv


async def get_links(path, limitation):
    print(path)
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        url_list = []

        for row in reader:
            url_list.append(row['URL'])

        if limitation != 0:
            url_list = url_list[:limitation]
        else:
            url_list = url_list
        return url_list
