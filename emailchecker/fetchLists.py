import requests


def run():
    email_lists = []

    with open("./emailchecker/email.list", "r") as file:
        for url in file:
            email_lists.append(url.strip())

    disposable_emails = []

    for url in email_lists:
        print("Fetching " + url)
        r = requests.get(url, timeout=120)
        for email in r.text.splitlines():
            if email.strip() != "" and not email.strip() in disposable_emails:
                disposable_emails.append(email.strip())
        print("Done Fetching")

    with open("./emailchecker/manual_blocklist.list", "r") as file:
        for email in file:
            if email.strip() != "" and not email.strip() in disposable_emails:
                disposable_emails.append(email.strip())

    with open("./emailchecker/disposable.list", "w") as file:
        file.truncate(0)
        for email in disposable_emails:
            file.write(email + "\n")


if __name__ == "__main__":
    run()
