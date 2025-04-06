import requests

URL = "http://localhost:8000/v1/user/"

# テストデータ
test_payload = {
    "id"  : "test_id",
    "name": "test_name",
}

def test_post_user():
    try:
        response = requests.post(URL, json=test_payload)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:", response.json())

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_post_user()