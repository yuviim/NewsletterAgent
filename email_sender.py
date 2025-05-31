import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def send_email(subject, body_html, to_emails):
    SMTP_SERVER = "smtp.mail.yahoo.com"
    SMTP_PORT = 587  # Use 465 for SSL
    SMTP_USER = os.getenv("EMAIL_SENDER")       # your Yahoo email, e.g., yourname@yahoo.com
    SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD") # your Yahoo password or app password

    if not all([SMTP_USER, SMTP_PASSWORD]):
        raise ValueError("Missing email credentials. Check environment variables.")

    for recipient in to_emails:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = recipient

        part = MIMEText(body_html, "html")
        msg.attach(part)

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # use starttls for port 587
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipient, msg.as_string())
            server.quit()
            print(f"✅ Email sent to {recipient}")
        except Exception as e:
            print(f"❌ Failed to send email to {recipient}: {e}")
            return False, str(e)
    return True, "Emails sent successfully"

@app.route("/send-email", methods=["POST"])
def send_email_api():
    try:
        data = request.json
        subject = data.get("subject")
        body_html = data.get("body_html")
        to_emails = data.get("to_emails")

        if not subject or not body_html or not to_emails:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        success, message = send_email(subject, body_html, to_emails)
        if success:
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": message}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    # Run this service independently
    app.run(host="0.0.0.0", port=5001)
