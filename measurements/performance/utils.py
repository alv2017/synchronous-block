from httpx import Client


def measure_response_time(url: str) -> float:
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