from flask import Flask, render_template
import imaplib
from email.parser import BytesParser
from email.policy import default

app = Flask(__name__)

# Function to fetch emails from an inbox
def fetch_emails(username, password, server, port, unread_only=True):
    emails = []
    connection = None

    try:
        connection = imaplib.IMAP4_SSL(server, port)
        connection.login(username, password)
        connection.select("inbox")

        criteria = "UNSEEN" if unread_only else "ALL"
        result, data = connection.search(None, criteria)

        if result == "OK":
            for num in data[0].split():
                result, message_data = connection.fetch(num, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE FLAGS)])")
                if result == "OK":
                    msg = BytesParser(policy=default).parsebytes(message_data[0][1])
                    flags = msg.get("flags", [])
                    unread = b"\\Seen" not in flags
                    emails.append({
                        "subject": msg.get("subject", ""),
                        "date": msg.get("date", ""),
                        "unread": unread,
                    })

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if connection:
            connection.logout()

    return emails


# Route for the dashboard
@app.route('/')
def dashboard():
    # Example usage for 4 email accounts
    email_account1 = {
        "username": "teja.czechsolutions@gmail.com",
        "password": "twlc alix xtnl knso",
        "server": "imap.gmail.com",
        "port": 993,
    }

    email_account2 = {
        "username": "anand.czechsolutions@gmail.com",
        "password": "pzqk ckgj fpnc jzrh",
        "server": "imap.gmail.com",
        "port": 993,
    }

    email_account3 = {
        "username": "walter.czechsolutions@gmail.com",
        "password": "zzqd eclz taru yile",
        "server": "imap.gmail.com",
        "port": 993,
    }

    # email_account4 = {
    #     "username": "anil.czechsolutions@gmail.com",
    #     "password": "wrdq ulwu xdik vcrf",
    #     "server": "imap.gmail.com",
    #     "port": 993,
    # }

    # Fetch emails for the first account
    emails1 = fetch_emails(**email_account1)

    # Fetch emails for the second account
    emails2 = fetch_emails(**email_account2)

    # Fetch emails for the third account   
    emails3 = fetch_emails(**email_account3)

    # Fetch emails for the fourth account   
    # emails4 = fetch_emails(**email_account4)

    return render_template('inbox_template.html', emails1=emails1, emails2=emails2, emails3=emails3)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
