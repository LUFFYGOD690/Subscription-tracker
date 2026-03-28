import json

FILE_NAME = "data.json"  # File where subscription data is stored

# Load data from JSON file
def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)  # Convert JSON to Python list
    except:
        return []  # Return empty list if file doesn't exist or error occurs

# Save data to JSON file
def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)  # Write formatted JSON