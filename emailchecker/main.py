import time
from os import getenv

from dotenv import load_dotenv

load_dotenv()
from slack_sdk.webhook import WebhookClient
from postgres import Postgres

from plemmy import LemmyHttp
from plemmy.responses import (
    ListRegistrationApplicationsResponse,
)

db = Postgres(url=getenv("DATABASE_URL"))

lemmy = LemmyHttp(getenv("LEMMY_URL"))
lemmy.login(getenv("LEMMY_USERNAME"), getenv("LEMMY_PASSWORD"))

disposable_emails = []

with open("emailchecker/disposable.list", "r") as file:
    for email in file.read().splitlines():
        if email.strip() != "" and not email.strip() in disposable_emails:
            disposable_emails.append(email.strip())

webhook = False
if getenv("SLACK_WEBHOOK_URL") != "":
    webhook = WebhookClient(getenv("SLACK_WEBHOOK_URL"))


def main():
    while True:
        print("Checking for new registrations")
        try:
            new_registrations = lemmy.list_registration_applications()
            registrations: ListRegistrationApplicationsResponse = ListRegistrationApplicationsResponse(
                new_registrations
            )
            for registration in registrations.registration_applications:
                try:
                    if registration.admin is not None:
                        continue
                    email_to_check = registration.creator_local_user.email
                    domain = email_to_check.split("@")[1]
                    user = registration.creator
                    if domain.strip() in disposable_emails:
                        print(f"User {user.name} got blocked for using a disposable email address ({email_to_check})")
                        if getenv("DENY_TRASH_MAILS") == "true":
                            lemmy.approve_registration_application(False, registration.id, "Disposable Email")
                        if webhook:
                            webhook.send(text=f"User {user.name} got blocked for using a disposable email address")
                    else:
                        lemmy.approve_registration_application(True, registration.id, "Not a disposable email")
                        if webhook:
                            webhook.send(text=f"User {user.name} got approved.")

                except Exception as e:
                    print("Error while checking for one registration")
                    print(e)
        except Exception as e:
            print("Error while checking for new registrations")
            print(e)

        print("Waiting for 60 Seconds...")
        time.sleep(60)