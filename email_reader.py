import json


def read_mock_emails(filename="data/mock_emails.json"):
    with open(filename, "r", encoding="utf-8") as file:
        emails = json.load(file)

    return emails