import requests
import sys
import random
import string

BASE_URL = "http://localhost:8000"


def generate_random_string(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def create_user():
    username = f"user_{generate_random_string()}"
    email = f"{username}@example.com"
    password = "Password123!"
    payload = {"username": username, "email": email, "password": password}
    response = requests.post(f"{BASE_URL}/users/", json=payload)
    if response.status_code == 201:
        return response.json(), password
    else:
        print(f"Failed to create user: {response.text}")
        sys.exit(1)


def login(email, password):
    payload = {"username": email, "password": password}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to login: {response.text}")
        sys.exit(1)


def main():
    try:
        print("Creating user...")
        user, password = create_user()
        email = user["email"]
        print(f"User created: {email}")

        print("Attempting login...")
        token_data = login(email, password)
        print(f"Login successful. Token: {token_data['access_token'][:20]}...")

        print("Success: Authentication verification passed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
