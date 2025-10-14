import random
import string
import time

from api.apps.auth.passwords import hash_password


def generate_password(length: int) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password


def generate_password_list(n: int = 10) -> [str]:
    return [generate_password(length=12) for _ in range(n)]


def hashing_experiment(repeat: int = 10):
    passwords_list = generate_password_list(n=repeat)
    start_time = time.perf_counter()
    hashed_passwords = [hash_password(p, rounds=12) for p in passwords_list]
    end_time = time.perf_counter()
    print("Average password hashing time in seconds:", (end_time - start_time) / repeat)
    return hashed_passwords


if __name__ == "__main__":
    hashing_experiment(repeat=10)
