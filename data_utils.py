import json

class DataUtils:
    @staticmethod
    def load_crawled_data(filename):
        """Utility function to load crawled data from a JSON file."""
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
