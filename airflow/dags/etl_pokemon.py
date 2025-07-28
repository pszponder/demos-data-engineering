import json
import logging
from datetime import datetime, timedelta
from typing import Any

import boto3
import requests
from airflow.sdk import dag, task
from botocore.exceptions import ClientError


# Utility functions for Pokemon API interactions
def fetch_pokemon_list(limit: int = 20, offset: int = 0) -> dict[str, Any]:
    """
    Fetch a list of Pokemon from the PokeAPI.

    Args:
        limit: Number of Pokemon to fetch
        offset: Starting offset for pagination

    Returns:
        Dictionary containing the API response
    """
    base_url = "https://pokeapi.co/api/v2/pokemon"

    try:
        response = requests.get(f"{base_url}?limit={limit}&offset={offset}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching Pokemon list: {str(e)}")
        raise


def fetch_pokemon_details(pokemon_url: str) -> dict[str, Any]:
    """
    Fetch detailed information for a specific Pokemon.

    Args:
        pokemon_url: URL to fetch Pokemon details from

    Returns:
        Dictionary containing detailed Pokemon information
    """
    try:
        response = requests.get(pokemon_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching Pokemon details from {pokemon_url}: {str(e)}")
        raise


def extract_pokemon_info(pokemon_detail: dict[str, Any]) -> dict[str, Any]:
    """
    Extract and format key information from Pokemon detail response.

    Args:
        pokemon_detail: Raw Pokemon detail data from API

    Returns:
        Formatted Pokemon information dictionary
    """
    return {
        "id": pokemon_detail["id"],
        "name": pokemon_detail["name"],
        "height": pokemon_detail["height"],
        "weight": pokemon_detail["weight"],
        "base_experience": pokemon_detail["base_experience"],
        "types": [type_info["type"]["name"] for type_info in pokemon_detail["types"]],
        "abilities": [
            ability["ability"]["name"] for ability in pokemon_detail["abilities"]
        ],
        "stats": {
            stat["stat"]["name"]: stat["base_stat"] for stat in pokemon_detail["stats"]
        },
    }


def get_pokemon_sample(limit: int = 20) -> dict[str, Any]:
    """
    Main utility function to extract a sample of Pokemon data.

    Args:
        limit: Number of Pokemon to extract

    Returns:
        Dictionary containing Pokemon data and metadata
    """
    try:
        # Get Pokemon list
        pokemon_list = fetch_pokemon_list(limit=limit)

        # Extract detailed information for each Pokemon
        detailed_pokemon = []

        for pokemon in pokemon_list["results"]:
            try:
                # Get detailed info for each Pokemon
                pokemon_detail = fetch_pokemon_details(pokemon["url"])

                # Extract and format key information
                pokemon_info = extract_pokemon_info(pokemon_detail)

                detailed_pokemon.append(pokemon_info)
                logging.info(f"Extracted data for Pokemon: {pokemon_info['name']}")

            except requests.RequestException as e:
                logging.error(f"Error fetching details for {pokemon['name']}: {str(e)}")
                continue

        result = {
            "count": len(detailed_pokemon),
            "pokemon_data": detailed_pokemon,
            "extraction_timestamp": datetime.now().isoformat(),
            "api_endpoint": "https://pokeapi.co/api/v2/pokemon",
        }

        logging.info(f"Successfully extracted data for {len(detailed_pokemon)} Pokemon")
        return result

    except Exception as e:
        logging.error(f"Unexpected error during Pokemon extraction: {str(e)}")
        raise


# # Utility functions for S3 operations
# def create_s3_client():
#     """
#     Create and return an S3 client.
#     Uses AWS credentials from environment variables or IAM roles.
#     """
#     try:
#         s3_client = boto3.client("s3")
#         return s3_client
#     except Exception as e:
#         logging.error(f"Error creating S3 client: {str(e)}")
#         raise


# def upload_json_to_s3(data: dict[str, Any], bucket_name: str, object_key: str) -> str:
#     """
#     Upload JSON data to S3.

#     Args:
#         data: Dictionary to upload as JSON
#         bucket_name: S3 bucket name
#         object_key: S3 object key (file path)

#     Returns:
#         S3 URI of the uploaded object
#     """
#     try:
#         s3_client = create_s3_client()

#         # Convert data to JSON string
#         json_data = json.dumps(data, indent=2, ensure_ascii=False)

#         # Upload to S3
#         s3_client.put_object(
#             Bucket=bucket_name,
#             Key=object_key,
#             Body=json_data,
#             ContentType="application/json",
#         )

#         s3_uri = f"s3://{bucket_name}/{object_key}"
#         logging.info(f"Successfully uploaded data to {s3_uri}")
#         return s3_uri

#     except ClientError as e:
#         logging.error(f"AWS S3 error uploading to {bucket_name}/{object_key}: {str(e)}")
#         raise
#     except Exception as e:
#         logging.error(f"Unexpected error uploading to S3: {str(e)}")
#         raise


# def generate_s3_key(timestamp: str, data_type: str = "pokemon") -> str:
#     """
#     Generate an S3 object key with timestamp partitioning.

#     Args:
#         timestamp: ISO timestamp string
#         data_type: Type of data for the key prefix

#     Returns:
#         S3 object key with date partitioning
#     """
#     dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

#     # Create partitioned key: data_type/year=YYYY/month=MM/day=DD/filename
#     key = (
#         f"{data_type}/"
#         f"year={dt.year}/"
#         f"month={dt.month:02d}/"
#         f"day={dt.day:02d}/"
#         f"{data_type}_{dt.strftime('%Y%m%d_%H%M%S')}.json"
#     )

#     return key


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

    # @task
    # def load_to_s3(pokemon_data) -> dict[str, str]:
    #     """
    #     Load Pokemon data to S3 bucket.

    #     Args:
    #         pokemon_data: Pokemon data from extract task

    #     Returns:
    #         Dictionary containing S3 upload information
    #     """
    #     # Configuration - you can modify these or use Airflow Variables/Connections
    #     bucket_name = "your-pokemon-data-bucket"  # Change this to your bucket name

    #     # Generate S3 key with timestamp partitioning
    #     s3_key = generate_s3_key(
    #         timestamp=pokemon_data["extraction_timestamp"], data_type="pokemon"
    #     )

    #     # Upload to S3
    #     s3_uri = upload_json_to_s3(
    #         data=pokemon_data, bucket_name=bucket_name, object_key=s3_key
    #     )

    #     result = {
    #         "s3_uri": s3_uri,
    #         "bucket_name": bucket_name,
    #         "object_key": s3_key,
    #         "upload_timestamp": datetime.now().isoformat(),
    #         "record_count": pokemon_data["count"],
    #     }

    #     logging.info(
    #         f"Successfully loaded {pokemon_data['count']} Pokemon records to {s3_uri}"
    #     )
    #     return result

    # @task
    # def log_pipeline_completion(
    #     extract_result: Dict[str, Any], s3_result: Dict[str, str]
    # ) -> None:
    #     """
    #     Log completion of the entire ETL pipeline.

    #     Args:
    #         extract_result: Result from extract task
    #         s3_result: Result from S3 upload task
    #     """
    #     logging.info("=== Pokemon ETL Pipeline Completed ===")
    #     logging.info(f"Extracted {extract_result['count']} Pokemon records")
    #     logging.info(
    #         f"Data extraction timestamp: {extract_result['extraction_timestamp']}"
    #     )
    #     logging.info(f"S3 upload location: {s3_result['s3_uri']}")
    #     logging.info(f"S3 upload timestamp: {s3_result['upload_timestamp']}")
    #     logging.info("Pipeline completed successfully!")

    @task
    def end():
        pass

    # Define task flow
    # extracted_data = extract_pokemon_sample()
    # s3_upload_result = load_to_s3(pokemon_data=extracted_data)
    # log_pipeline_completion(extracted_data, s3_upload_result)

    (start() >> extract_pokemon_sample() >> end())


# Instantiate the DAG
pokemon_dag = pokemon_etl()
