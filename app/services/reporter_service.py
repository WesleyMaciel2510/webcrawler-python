import os
import requests
from typing import List
from dotenv import load_dotenv
from app.models.reporter import Reporter

# Load environment variables from .env file
load_dotenv()

class ReportersService:
    def __init__(self):
        self.elastic_url = os.getenv("ELASTIC_URL")
        self.elastic_token = os.getenv("ELASTIC_TOKEN")

    def get_reporters(self) -> List[Reporter]:
        try:
            # Make a POST request to Elasticsearch
            response = requests.post(
                self.elastic_url,
                json={
                    "size": 1000,
                    "_source": ["reporter"],  # Fetch only the "reporter" field
                    "query": {
                        "match_all": {},  # Return all documents
                    },
                },
                headers={
                    "Authorization": f"ApiKey {self.elastic_token}",
                    "Content-Type": "application/json",
                },
            )

            # Raise an exception for HTTP errors
            response.raise_for_status()

            # Extract reporters from the response
            hits = response.json()["hits"]["hits"]
            reporter_names = [hit["_source"]["reporter"] for hit in hits]

            # Remove duplicates and sort
            unique_reporter_names = sorted(list(set(reporter_names)))

            # Transform into Reporter objects
            reporters = [Reporter(name=name, organization="Unknown") for name in unique_reporter_names]

            return reporters

        except requests.RequestException as e:
            print(f"Error fetching reporters: {e}")
            raise ValueError("Error fetching reporters")