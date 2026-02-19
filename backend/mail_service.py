from email.message import EmailMessage
import smtplib
import os

def send_email():
  print("Sending email...")
  try:
    sender = os.getenv("MAILTRAP_SENDER", "from@example.com")
    receiver = os.getenv("MAILTRAP_RECEIVER", "to@example.com")

    host = os.getenv("MAILTRAP_HOST", "sandbox.smtp.mailtrap.io")
    port = int(os.getenv("MAILTRAP_PORT", "2525"))
    username = os.getenv("MAILTRAP_USERNAME")
    password = os.getenv("MAILTRAP_PASSWORD")
    use_ssl = os.getenv("MAILTRAP_USE_SSL", "False") == "True"
    use_starttls = os.getenv("MA()ILTRAP_STARTTLS", "True") == "True"

    if not username or not password:
      return {
        "success": False,
        "message": "MAILTRAP_USERNAME and MAILTRAP_PASSWORD are required"
      }

    msg = EmailMessage()
    msg["Subject"] = "Hi Mailtrap"
    msg["To"] = receiver
    msg["From"] = sender
    msg.set_content("This is a test e-mail message.")

    if use_ssl:
      with smtplib.SMTP_SSL(host, port, timeout=10) as server:
        server.login(username, password)
        server.send_message(msg)
    else:
      with smtplib.SMTP(host, port, timeout=10) as server:
        server.ehlo()
        if use_starttls and server.has_extn("starttls"):
          server.starttls()
          server.ehlo()
        server.login(username, password)
        server.send_message(msg)

    return {
      "success": True,
      "message": "Mail sent successfully"
    }
  except Exception as e:
    print(f"Error sending email: {str(e)}")
    return {
      "success": False,
      "message": "Failed to send email: " + str(e)
    }



