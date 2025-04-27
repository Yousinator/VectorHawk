from vectorhawk.data.ingestion import Ingestion
from vectorhawk.data.processing_pipeline import PreprocessingPipeline
from vectorhawk.core.logger import logger


ingest = Ingestion()
preprocess = PreprocessingPipeline()

def run_pipeline():
    logger.info("Starting VectorHawk ingestion test...")

    # Run CVE ingestion
    logger.info("Ingesting CVE data...")
    raw_cve_data = ingest.ingest_cve()
    # logger.info("Ingesting MITRE data...")
    # raw_mitre_data = ingest.ingest_mitre()

    if raw_cve_data != []:
        logger.info("Preprocessing CVE data...")
        preprocess.process_cve_data()

    # if raw_mitre_data:
    #     logger.info("Ingesting MITRE data...")
    #     preprocess.process_mitre_data()

run_pipeline()
