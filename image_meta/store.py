import json
import csv


def store_seal_img_metadata(folder, id):
    metadata_file = 'metadata.csv'
    file_path = folder + '/' + metadata_file

    with open(file_path, 'a+') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([id])

    csv_file.close()


def store_seal_metadata(folder, seal_name):
    seal_name_file = 'seals.csv'
    file_path = folder + '/' + seal_name_file
    with open(file_path, 'a+') as csv_file:
        csv_reader = csv.reader(csv_file)
        name_exists = False
        for row in csv_reader:
            print row[0]
            if row[0] == seal_name:
                name_exists = True
                break

        if not name_exists:
            writer = csv.writer(csv_file)
            writer.writerow([seal_name])

    csv_file.close()
