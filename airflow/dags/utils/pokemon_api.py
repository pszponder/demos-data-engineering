"""
Pokemon API utility functions for fetching and processing Pokemon data.
"""

import logging
from datetime import datetime
from typing import Any

import requests


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
