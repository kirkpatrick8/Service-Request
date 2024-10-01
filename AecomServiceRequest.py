import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# Streamlit settings
st.set_page_config(page_title="AECOM Service Information Request", page_icon="📧", layout="wide")

# Outlook SMTP settings
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SENDER_EMAIL = "mark.kirkpatrick@aecom.com"  # Replace with your actual email
SENDER_PASSWORD = "Beth2024"  # Replace with your actual app password

# Recipient emails
RECIPIENTS = {
    "NIE": "Markups@nienetworks.co.uk",
    "Phoenix": "dialbeforeyoudig@phoenixnaturalgas.com",
    "Firmus": "dialb4udig@firmusenergy.co.uk",
    "VM": "PlantEnquiriesTeam@virginmedia.co.uk",
    "Northern": "dfiroads.northern@infrastructure-ni.gov.uk",
    "Southern": "dfiroads.southern@infrastructure-ni.gov.uk",
    "Eastern": "dfiroads.eastern@infrastructure-ni.gov.uk",
    "Western": "dfiroads.western@infrastructure-ni.gov.uk",
    "Greater Belfast": "rivers.belfast@infrastructure-ni.gov.uk",
    "Lisburn": "rivers.lisburn@infrastructure-ni.gov.uk",
    "Coleraine": "rivers.coleraine@infrastructure-ni.gov.uk",
    "Armagh": "rivers.armagh@infrastructure-ni.gov.uk",
    "Fermanagh": "rivers.fermanagh@infrastructure-ni.gov.uk",
    "Omagh": "rivers.omagh@infrastructure-ni.gov.uk"
    "test" : "hannah.finlay@aecom.com"
}

def create_email_body(sender_name, location, return_email):
    return f"""To whom it may concern,

We are planning work in the {location} area. I have attached a location map to show where we would require service information. I would be obliged if you could provide me with details of any existing services at this location and within the surrounding area.

I trust you find this satisfactory, however if you should require any additional information or clarification, please do not hesitate to contact me at {return_email}.

Best regards,
{sender_name}"""

def send_email(sender_name, location, attachment, return_email, selected_recipients, custom_emails):
    msg = MIMEMultipart()
    msg['From'] = f"{sender_name} via AECOM <{SENDER_EMAIL}>"
    msg['Subject'] = f"Service Information Request - {location}"
    msg['Reply-To'] = return_email

    body = create_email_body(sender_name, location, return_email)
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
    msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            for recipient in selected_recipients:
                msg['To'] = RECIPIENTS[recipient]
                server.send_message(msg)
                st.success(f"Email sent successfully to {recipient}")
            for email in custom_emails:
                msg['To'] = email
                server.send_message(msg)
                st.success(f"Email sent successfully to {email}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("AECOM Service Information Request")

    col1, col2 = st.columns(2)

    with col1:
        with st.form(key='email_form'):
            sender_name = st.text_input("Your Name")
            location = st.text_input("Work Location")
            return_email = st.text_input("Return Email Address")
            selected_recipients = st.multiselect("Select Recipients", options=list(RECIPIENTS.keys()))
            custom_emails = st.text_area("Custom Email Addresses (one per line)")
            uploaded_file = st.file_uploader("Upload Location Map", type=["pdf", "jpg", "png"])
            submit_button = st.form_submit_button(label="Send Emails")

    with col2:
        st.subheader("Email Preview")
        if sender_name and location and return_email:
            preview = create_email_body(sender_name, location, return_email)
            st.text_area("Email Content", preview, height=300)
        else:
            st.info("Fill in the form to see the email preview")

        st.subheader("Selected Recipients")
        for recipient in selected_recipients:
            st.write(f"- {recipient}: {RECIPIENTS[recipient]}")
        
        custom_email_list = [email.strip() for email in custom_emails.split('\n') if email.strip()]
        if custom_email_list:
            st.subheader("Custom Email Addresses")
            for email in custom_email_list:
                st.write(f"- {email}")

    if submit_button:
        if sender_name and location and return_email and uploaded_file and (selected_recipients or custom_email_list):
            with st.spinner("Sending emails..."):
                # Save uploaded file temporarily
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                send_email(sender_name, location, uploaded_file.name, return_email, selected_recipients, custom_email_list)
                
                # Remove temporary file
                os.remove(uploaded_file.name)
        else:
            st.warning("Please fill in all required fields, select at least one recipient or add a custom email, and upload a location map.")

    # Footer with contact information
    st.markdown("---")
    st.markdown("Made by [Mark Kirkpatrick](mailto:mark.kirkpatrick@aecom.com)")
    st.markdown("For any queries, please email [mark.kirkpatrick@aecom.com](mailto:mark.kirkpatrick@aecom.com)")

if __name__ == "__main__":
    main()
