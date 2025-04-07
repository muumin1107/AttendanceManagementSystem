import requests

URL = "http://localhost:8000/v1/attendance/"

def test_get_attendance():
    try:
        response = requests.get(URL)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:", response.json())

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_get_attendance()