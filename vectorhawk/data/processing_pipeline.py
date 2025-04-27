from vectorhawk.data.storage import ElasticsearchHandler
from vectorhawk.core.logger import logger
from vectorhawk.core.config import Config

class PreprocessingPipeline:
    def __init__(self):
        self.logger = logger
        self.storage = ElasticsearchHandler()
        self.config = Config()
        self.es = self.storage.es

    def process_cve_data(self, raw_index="raw-cve-data", processed_index="processed-cve-data"):
        try:
            # Fetch raw documents
            response = self.es.search(index=raw_index, body={"query": {"match_all": {}}}, size=10000)

            hits = response.get('hits', {}).get('hits', [])
            if not hits:
                logger.warning(f"No documents found in {raw_index}.")
                return

            processed_docs = []
            delete_actions = []

            for hit in hits:
                source = hit["_source"].get("cve", {})

                # Extract fields
                cve_id = source.get("id")
                published = source.get("published")
                last_modified = source.get("lastModified")
                vuln_status = source.get("vulnStatus")

                # Get English description if available
                description = next((desc["value"] for desc in source.get("descriptions", []) if desc["lang"] == "en"), None)

                # Extract CVSS (if available)
                metrics = source.get("metrics", {}).get("cvssMetricV31", [])
                if metrics:
                    cvss = metrics[0].get("cvssData", {})
                    base_score = cvss.get("baseScore")
                    base_severity = cvss.get("baseSeverity")
                    vector_string = cvss.get("vectorString")
                else:
                    base_score = base_severity = vector_string = None

                # Extract Weakness (CWE) if available
                weaknesses = source.get("weaknesses", [])
                if weaknesses:
                    weakness = weaknesses[0].get("description", [{}])[0].get("value")
                else:
                    weakness = None

                # Extract references (urls)
                references = [ref["url"] for ref in source.get("references", [])]

                # Build the processed document
                processed_doc = {
                    "cve_id": cve_id,
                    "published": published,
                    "last_modified": last_modified,
                    "vuln_status": vuln_status,
                    "description": description,
                    "base_score": base_score,
                    "base_severity": base_severity,
                    "vector_string": vector_string,
                    "weakness": weakness,
                    "references": references
                }

                processed_docs.append(processed_doc)

                # Check if the same CVE already exists in the processed index
                exists_query = {
                    "query": {
                        "term": {
                            "cve_id.keyword": cve_id
                        }
                    }
                }



                # Add delete action for the raw document if no duplicate is found
                delete_actions.append({
                    "delete": {
                        "_index": raw_index,
                        "_id": hit["_id"]
                    }
                })

            # Bulk insert into processed index
            actions = [{"index": {"_index": processed_index}} for _ in processed_docs]

            bulk_data = []
            for action, doc in zip(actions, processed_docs):
                bulk_data.append(action)
                bulk_data.append(doc)

            # Actually send the bulk request for processed data
            if bulk_data:
                self.es.bulk(body=bulk_data)
                logger.info(f"Stored {len(processed_docs)} processed CVE documents to {processed_index}.")
            else:
                logger.warning("No processed documents to store.")

            # Now delete the processed documents from the raw index
            if delete_actions:
                delete_bulk_data = []
                for action in delete_actions:
                    delete_bulk_data.append(action)

                # Send the delete bulk request
                if delete_bulk_data:
                    self.es.bulk(body=delete_bulk_data)
                    logger.info(f"Deleted {len(delete_actions)} documents from {raw_index}.")
                else:
                    logger.warning("No documents to delete from the raw index.")

        except Exception as e:
            logger.error(f"Failed to process CVE data: {e}")



    def transform_mitre(self, doc: dict) -> dict:
        """Transform raw MITRE document into a structured format."""
        # TODO: Add real transformation logic
        return {
            "id": doc.get("attack_id"),
            "tactic": doc.get("tactic"),
            "technique": doc.get("technique"),
            "platform": doc.get("platform"),
        }

    def process_mitre_data(self) -> list[dict]:
        try:
            raw_docs = self.storage.search_documents("raw-mitre-data", {"match_all": {}})
            self.logger.info(f"Processing {len(raw_docs)} MITRE documents")
            return [self.transform_mitre(doc["_source"]) for doc in raw_docs]
        except Exception as e:
            self.logger.error(f"Failed to process MITRE data: {e}")
            return []
