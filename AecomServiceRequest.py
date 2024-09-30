import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# Outlook SMTP settings
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_outlook_email@yourcompany.com"
SENDER_PASSWORD = "your_app_password"  # Use an app password for security

# Recipient emails
RECIPIENTS = {
    "NIE": "Markups@nienetworks.co.uk",
    "Phoenix": "dialbeforeyoudig@phoenixnaturalgas.com",
    "Firmus": "dialb4udig@firmusenergy.co.uk",
    "VM": "PlantEnquiriesTeam@virginmedia.co.uk"
}

def send_email(sender_name, location, attachment):
    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} via Company <{SENDER_EMAIL}>"
    msg['Subject'] = f"Service Information Request - {location}"

    # Email body
    body = f"""To whom it may concern,

We are planning work in the {location} area. I have attached a location map to show where we would require service information. I would be obliged if you could provide me with details of any existing services at this location and within the surrounding area.

I trust you find this satisfactory, however if you should require any additional information or clarification, please do not hesitate to contact me.

Best regards,
{sender_name}"""

    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(attachment, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
    msg.attach(part)

    # Send emails
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            for company, email in RECIPIENTS.items():
                msg['To'] = email
                server.send_message(msg)
                st.success(f"Email sent successfully to {company}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("Service Information Request Email Sender")

    sender_name = st.text_input("Your Name")
    location = st.text_input("Work Location")
    
    uploaded_file = st.file_uploader("Upload Location Map", type=["pdf", "jpg", "png"])
    
    if st.button("Send Emails") and sender_name and location and uploaded_file:
        # Save uploaded file temporarily
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        send_email(sender_name, location, uploaded_file.name)
        
        # Remove temporary file
        os.remove(uploaded_file.name)
    elif st.button("Send Emails"):
        st.warning("Please fill in all fields and upload a location map.")

if __name__ == "__main__":
    main()
