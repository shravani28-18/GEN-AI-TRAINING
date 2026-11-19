import sys

import requests


def check_api():
    response = requests.get(
        "http://localhost:8000/health",
        timeout=10,
    )
    response.raise_for_status()
    print("PASS: API health check")


def check_ui():
    response = requests.get(
        "http://localhost:8501",
        timeout=10,
    )
    response.raise_for_status()
    print("PASS: Streamlit UI check")


if __name__ == "__main__":
    try:
        check_api()
        check_ui()
        print("\nAll Docker smoke tests passed!")

    except requests.RequestException as error:
        print(f"FAIL: {error}")
        sys.exit(1)