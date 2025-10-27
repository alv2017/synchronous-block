import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(project_root)


if __name__ == "__main__":
    from measurements.performance import measure_get_response_time
    N = 100  # Number of requests to send
    url = "http://127.0.0.1:8000/api/health/"
    total_time = 0.0
    for _ in range(100):
        total_time += measure_get_response_time(url)
    print(f"Average response time over {N} requests: {total_time / N:.6f} seconds")