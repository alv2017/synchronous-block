from httpx import Client


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