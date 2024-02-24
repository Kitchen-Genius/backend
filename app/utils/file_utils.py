import json

## TODO - change this to caching in database.
def save_data_locally(data, filename):
    with open(f'app/jsons/{filename}', 'w') as file:
        json.dump(data, file, indent=4)