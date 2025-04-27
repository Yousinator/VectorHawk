import requests
from vectorhawk.core.logger import logger
from vectorhawk.data.storage import ElasticsearchHandler
from vectorhawk.core.config import Config
from taxii2client.v21 import Server
from stix2 import TAXIICollectionSource
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime, timedelta
import requests

class Ingestion():
    def __init__(self):
        self.config = Config()

        # Define endpoints
        self.CVE_API_ENDPOINT = self.config.CVE_API_ENDPOINT
        self.MITRE_DISCOVERY_URL = self.config.MITRE_DISCOVERY_URL
        self.es = ElasticsearchHandler()
        self.CVE_API_KEY = self.config.CVE_API_KEY


    def fetch_cve_data(self, params=None):
        """Fetch CVE data from the NVD API."""
        try:
            if not params:
                now = datetime.utcnow()
                start_date = (now - timedelta(days=30)).isoformat(timespec='milliseconds') + 'Z'
                end_date = now.isoformat(timespec='milliseconds') + 'Z'
                params = {
                    "pubStartDate": start_date,
                    "pubEndDate": end_date
                }

            headers = {"apiKey": self.CVE_API_KEY} if self.CVE_API_KEY else {}
            response = requests.get(self.CVE_API_ENDPOINT, headers=headers, params=params)
            response.raise_for_status()

            logger.info("Successfully fetched CVE data.")
            return response.json().get("vulnerabilities", [])

        except Exception as e:
            logger.error(f"Failed to fetch CVE data: {e}")
            return []



    def fetch_mitre_data(self, collection_name="Enterprise ATT&CK"):
        try:
            # Setup a session with retry and timeout handling
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount("https://", adapter)
            session.mount("http://", adapter)

            # Connect to MITRE TAXII server
            server = Server(self.MITRE_DISCOVERY_URL)  # No session argument here
            logger.info("Connected to MITRE TAXII server.")

            # Get the API root (there's usually just one)
            api_root = server.api_roots[0]
            logger.info(f"API Root discovered: {api_root.url}")

            # Discover the desired collection
            collections = api_root.collections
            target_collection = next((col for col in collections if collection_name.lower() in col.title.lower()), None)

            if not target_collection:
                logger.error(f"Collection '{collection_name}' not found.")
                return []

            logger.info(f"Fetching from collection: {target_collection.title}")

            # Use STIX2's TAXIICollectionSource to fetch and parse the data
            source = target_collection.get_objects()
            stix_objs = source

            logger.info(f"Fetched {len(stix_objs)} MITRE ATT&CK records.")
            return stix_objs

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while connecting to MITRE TAXII: {e}")
        except Exception as e:
            logger.error(f"Failed to fetch MITRE data from TAXII: {e}")
        return []


    def ingest_cve(self):
        """Ingest raw CVE data into Elasticsearch."""
        raw_cves = self.fetch_cve_data()
        print(raw_cves)
        if raw_cves:
            try:
                self.es.store_raw_data(index="raw-cve-data", documents=raw_cves)
                logger.info(f"Ingested {len(raw_cves)} CVE records.")
            except Exception as e:
                logger.error(f"Failed to store CVE data: {e}")

    def ingest_mitre(self):
        """Ingest raw MITRE data into Elasticsearch."""
        raw_mitre = self.fetch_mitre_data()
        if raw_mitre:
            try:
                self.es.store_raw_data(index="raw-mitre-data", documents=raw_mitre)
                logger.info(f"Ingested {len(raw_mitre)} MITRE records.")
            except Exception as e:
                logger.error(f"Failed to store MITRE data: {e}")
