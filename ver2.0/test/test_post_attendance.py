import requests

URL = "http://localhost:8000/v1/attendance/"

# テストデータ（必要に応じて変更OK）
test_payload = {
    "nfc_id": "test_post_attendance",
    "status": "test_post_attendance",
}

def test_post_attendance():
    try:
        response = requests.post(URL, json=test_payload)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:", response.json())
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_post_attendance()