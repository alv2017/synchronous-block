import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(project_root)


if __name__ == "__main__":
    from measurements.performance import (
        generate_username,
        generate_password,
        measure_post_response_time
    )
    N = 100  # Number of requests to send
    # Generate username and password pairs for POST data
    credentials = []
    for _ in range(100):
        username = generate_username()
        password = generate_password()
        credentials.append({
            "username": username,
            "password": password,
            "email": f"{username}@example.com"
        })

    url = "http://127.0.0.1:8000/api/users/register/"
    total_time = 0.0
    for _ in range(100):
        total_time += measure_post_response_time(url, data=credentials[_])
    print(f"Average response time over {N} requests: {total_time / N:.6f} seconds")