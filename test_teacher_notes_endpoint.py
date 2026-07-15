import requests


BASE_URL = "https://teachersnotes.pythonanywhere.com"
ENDPOINT = "/api/v1/teacher-notes"


url = BASE_URL + ENDPOINT


params = {
    "school": "Udavi",
    "grade": "6th",
    "start_date": "2026-07-01",
    "end_date": "2026-07-06"
}


print("API URL:")
print(url)

print("\nSending request...")


try:
    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    print("\nStatus Code:")
    print(response.status_code)

    print("\nResponse:")
    print(response.text)


except Exception as e:
    print("ERROR:")
    print(e)