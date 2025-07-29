import logging
import os
from datetime import datetime, timedelta
from typing import Any

from airflow.sdk import dag, task
from utils.pokemon_api import get_pokemon_sample
from utils.s3 import generate_s3_key, upload_json_to_s3

# Default arguments for the DAG
default_args = {
    "owner": "data-engineering-team",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="etl_pokemon",
    default_args=default_args,
    description="ETL pipeline to extract Pokemon data from PokeAPI and load to S3",
    schedule=timedelta(days=1),
    catchup=False,
    tags=["pokemon", "etl", "s3"],
)
def pokemon_etl():
    """
    Pokemon ETL DAG using modern Airflow decorators with separated utility functions
    """

    @task
    def start():
        pass

    @task
    def extract_pokemon_sample() -> dict[str, Any]:
        """
        Extract a sample of Pokemon data from the PokeAPI using utility functions.
        Returns the JSON results as a Python dictionary for XCom.
        """
        return get_pokemon_sample(limit=20)

    @task
    def load_to_s3(pokemon_data) -> dict[str, str]:
        """
        Load Pokemon data to S3 bucket.

        Args:
            pokemon_data: Pokemon data from extract task

        Returns:
            Dictionary containing S3 upload information
        """
        # Get bucket name from environment variables
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME must be set in environment variables")

        # Generate S3 key with timestamp partitioning
        s3_key = generate_s3_key(
            timestamp=pokemon_data["extraction_timestamp"], data_type="pokemon"
        )

        # Upload to S3
        s3_uri = upload_json_to_s3(
            data=pokemon_data, bucket_name=bucket_name, object_key=s3_key
        )

        result = {
            "s3_uri": s3_uri,
            "bucket_name": bucket_name,
            "object_key": s3_key,
            "upload_timestamp": datetime.now().isoformat(),
            "record_count": pokemon_data["count"],
        }

        logging.info(
            f"Successfully loaded {pokemon_data['count']} Pokemon records to {s3_uri}"
        )
        return result

    @task
    def end():
        pass

    # Define task flow
    extracted_data = extract_pokemon_sample()
    s3_upload_result = load_to_s3(pokemon_data=extracted_data)

    (start() >> extracted_data >> s3_upload_result >> end())


# Instantiate the DAG
pokemon_dag = pokemon_etl()
