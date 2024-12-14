import requests

API_1_VALIDATE_URL = "http://127.0.0.1:8000/api/validate-token/"
API_2_CHAT_URL = "http://127.0.0.1:8001/api/chat/"

TOKEN = "7982f89ba385157ab4f1c90b9957b2f8c98c9100"

def validate_token():
    headers = {"Authorization": f"Token {TOKEN}"}
    response = requests.post(API_1_VALIDATE_URL, headers=headers)
    if response.status_code == 200:
        print(f"API 1 - Token Validated: {response.json()}")
    else:
        print(f"API 1 - Token Validation Failed: {response.json()}")

def test_chat_endpoint():
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"message": "Hello from API 1 to API 2"}
    response = requests.post(API_2_CHAT_URL, headers=headers, json=data)
    print("\nAPI 2 - Chat Endpoint Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    validate_token()
    test_chat_endpoint()
