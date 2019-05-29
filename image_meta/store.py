import json


def store_seal_img_metadata(folder, id):

    json_file = 'metadata.json'
    file_path = folder + '/' + json_file
    with open(file_path, 'a+') as json_file:
        try:
            imgs = json.load(json_file)
        except ValueError:
            imgs = []

        json.dump([], json_file)
        imgs.append({
            "id": id
        })
        json.dump(imgs, json_file)
