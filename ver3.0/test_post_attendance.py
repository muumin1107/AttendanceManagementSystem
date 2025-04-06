import requests

URL = "http://localhost:8000/v1/attendance/"

# テストデータ
test_payload = {
    "nfc_id": "test-nfc_id",
    "status": "clock_in",
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