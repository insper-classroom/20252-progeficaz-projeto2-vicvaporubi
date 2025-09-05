import json


def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data


def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)
    return True
