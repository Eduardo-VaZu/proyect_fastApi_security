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


def login_and_check_cookie(email, password):
    payload = {"username": email, "password": password}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    if response.status_code == 200:
        cookies = response.cookies
        if "access_token" in cookies:
            print("Success: 'access_token' cookie found in response.")
            return cookies
        else:
            print("Failure: 'access_token' cookie NOT found in response.")
            sys.exit(1)
    else:
        print(f"Failed to login: {response.text}")
        sys.exit(1)


def main():
    try:
        print("Creating user...")
        user, password = create_user()
        email = user["email"]
        print(f"User created: {email}")

        print("Attempting login and checking cookies...")
        cookies = login_and_check_cookie(email, password)

        print("Success: Cookie authentication verification passed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
