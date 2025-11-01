import string

from httpx import Client
from random import choices


def generate_string(length: int, symbols: str):
    """
    Generates a random string of specified length using the provided symbols.

    Args:
        length (int): The length of the string to generate.
        symbols (str): A string containing the symbols to use for generating the random string.

    Returns:
        str: A randomly generated string.
    """
    return "".join(choices(symbols, k=length))


def generate_username(length: int | None = None):
    min_length = 3
    max_length = 20
    symbols = string.ascii_letters + string.digits + "._-"
    if not length:
        length = choices(range(min_length, max_length + 1), k=1)[0]
    return generate_string(length, symbols)


def generate_password(length: int | None = None):
    min_length = 8
    max_length = 32
    symbols = string.ascii_letters + string.digits + string.punctuation
    if not length:
        length = choices(range(min_length, max_length + 1), k=1)[0]
    return generate_string(length, symbols)


def measure_get_response_time(url: str) -> float:
    """
    Measures the response time of a given API endpoint.

    Args:
        url (str): The URL of the API endpoint to measure.

    Returns:
        float: The response time in seconds.
    """
    with Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.elapsed.total_seconds()


def measure_post_response_time(url: str, data: dict) -> float:
    """
    Measures the response time of a given API endpoint for POST requests.

    Args:
        url (str): The URL of the API endpoint to measure.
        data (dict): The data to be sent in the POST request.

    Returns:
        float: The response time in seconds.
    """
    with Client() as client:
        response = client.post(url, json=data)
        response.raise_for_status()
        return response.elapsed.total_seconds()
