import json


def save_data_locally(data, filename):
    """test function to save localy for tests and logs."""
    with open(f'app/jsons/{filename}', 'w') as file:
        json.dump(data, file, indent=4)