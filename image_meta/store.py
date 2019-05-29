import json
import csv


def store_seal_img_metadata(folder, id):
    json_file = 'metadata.csv'
    file_path = folder + '/' + json_file

    with open(file_path, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([id])

    csvFile.close()
