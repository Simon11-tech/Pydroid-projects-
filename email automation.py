import smtplib
from email.message import EmailMessage

# 📝 Email configuration
EMAIL_ADDRESS = "eromoselesimon5@gmail.com"         # 👉 Your Gmail
EMAIL_PASSWORD = "nbhrdjkwnitzxnnr"           # 👉 Use Gmail App Password

# 📨 Compose message
msg = EmailMessage()
msg['Subject'] = "Automated Email from Python"
msg['From'] = EMAIL_ADDRESS
msg['To'] = "godswilleromosele3@gmail.com"        # 👉 Receiver's email
msg.set_content("Hello,\n\nThis email was sent using Python and Gmail SMTP!\n\n- Python Bot 🤖")

try:
    # 🌐 Connect to Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("✅ Email sent successfully!")

except Exception as e:
    print("❌ Error:", e)