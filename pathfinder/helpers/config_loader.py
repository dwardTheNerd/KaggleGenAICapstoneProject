import json
import os

def load_config(file_path):
    """Loads configuration data from a JSON file."""
    if not os.path.exists(file_path):
        # Handle the case where the file doesn't exist
        print(f"Error: Configuration file not found at {file_path}")
        return None
    
    try:
        # Open the file in read mode ('r')
        with open(file_path, 'r') as f:
            # Use json.load() to parse the JSON data from the file
            config = json.load(f)
            return config
    except json.JSONDecodeError:
        # Handle invalid JSON format
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        # Handle other potential errors (e.g., permission issues)
        print(f"An unexpected error occurred: {e}")
        return None