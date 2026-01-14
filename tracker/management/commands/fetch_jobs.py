from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Job
import imaplib
import email
import re

EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"

class Command(BaseCommand):
    help = "Fetch job applications from email"

    def handle(self, *args, **kwargs):
        print("fetch_jobs command started")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, '(SUBJECT "application")')

        user = User.objects.first()  # demo user

        for num in messages[0].split():
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            subject = msg["subject"]
            body = self.get_body(msg)

            company, role = self.extract_details(subject + body)

            if company and role:
                Job.objects.get_or_create(
                    user=user,
                    company=company,
                    role=role,
                    status="Applied"
                )

        mail.logout()
        self.stdout.write(self.style.SUCCESS("Jobs fetched successfully"))

    def get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return ""

    def extract_details(self, text):
        company_match = re.search(r"at\s+([A-Za-z0-9 &]+)", text)
        role_match = re.search(r"for\s+([A-Za-z0-9 &]+)", text)

        company = company_match.group(1) if company_match else None
        role = role_match.group(1) if role_match else "Software Engineer"

        return company, role
