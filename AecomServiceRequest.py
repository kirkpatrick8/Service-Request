import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# Streamlit settings
st.set_page_config(page_title="AECOM Service Information Request", page_icon="📧")

# Outlook SMTP settings
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SENDER_EMAIL = st.secrets["OUTLOOK_EMAIL"]
SENDER_PASSWORD = st.secrets["OUTLOOK_PASSWORD"]

# Recipient emails
RECIPIENTS = {
    "NIE": "Markups@nienetworks.co.uk",
    "Phoenix": "dialbeforeyoudig@phoenixnaturalgas.com",
    "Firmus": "dialb4udig@firmusenergy.co.uk",
    "VM": "PlantEnquiriesTeam@virginmedia.co.uk"
}

def send_email(sender_name, location, attachment):
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} via AECOM <{SENDER_EMAIL}>"
    msg['Subject'] = f"Service Information Request - {location}"

    body = f"""To whom it may concern,

We are planning work in the {location} area. I have attached a location map to show where we would require service information. I would be obliged if you could provide me with details of any existing services at this location and within the surrounding area.

I trust you find this satisfactory, however if you should require any additional information or clarification, please do not hesitate to contact me.

Best regards,
{sender_name}"""

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
    msg.attach(part)

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
    st.title("AECOM Service Information Request")

    with st.form(key='email_form'):
        sender_name = st.text_input("Your Name")
        location = st.text_input("Work Location")
        uploaded_file = st.file_uploader("Upload Location Map", type=["pdf", "jpg", "png"])
        submit_button = st.form_submit_button(label="Send Emails")

    if submit_button:
        if sender_name and location and uploaded_file:
            with st.spinner("Sending emails..."):
                # Save uploaded file temporarily
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                send_email(sender_name, location, uploaded_file.name)
                
                # Remove temporary file
                os.remove(uploaded_file.name)
        else:
            st.warning("Please fill in all fields and upload a location map.")

if __name__ == "__main__":
    main()
