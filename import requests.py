import requests

url = "https://teachersnotes.pythonanywhere.com//api/v1/teacher-notes"

response = requests.get(
    url,
    params={
        "school":"Udavi",
        "startDate":"2026-07-01",
        "endDate":"2026-07-06"
    }
)

print(response.status_code)
print(response.text)