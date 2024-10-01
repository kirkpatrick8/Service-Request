import streamlit as st
import msal
import requests
import base64
import os

# Streamlit settings
st.set_page_config(page_title="AECOM Service Information Request", page_icon="📧", layout="wide")

# Azure AD App Registration details
CLIENT_ID = "9dc71e18-a76a-4f05-9eb0-2f0a5c3b92e5"
CLIENT_SECRET = "LXG8Q~WDCbehS6beg..adkAszboKK3GwaJvyjcSL"
TENANT_ID = "16ed5ab4-2b59-4e40-806d-8a30bdc9cf26"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ['https://graph.microsoft.com/Mail.Send']

# Microsoft Graph API endpoint
GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Sender email
SENDER_EMAIL = "markkirkpatrick@aecom.com"

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
}

# Initialize MSAL client
msal_client = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

def get_token():
    result = msal_client.acquire_token_silent(SCOPES, account=None)
    if not result:
        result = msal_client.acquire_token_for_client(scopes=SCOPES)
    if "access_token" in result:
        return result['access_token']
    else:
        st.error(f"Failed to acquire token: {result.get('error')} - {result.get('error_description')}")
        return None

def send_email(token, sender_name, location, attachment, return_email, selected_recipients, custom_emails):
    # Read attachment
    with open(attachment, 'rb') as file:
        attachment_content = base64.b64encode(file.read()).decode('utf-8')

    # Prepare email message
    email_body = f"""To whom it may concern,

We are planning work in the {location} area. I have attached a location map to show where we would require service information. I would be obliged if you could provide me with details of any existing services at this location and within the surrounding area.

I trust you find this satisfactory, however if you should require any additional information or clarification, please do not hesitate to contact me at {return_email}.

Best regards,
{sender_name}"""

    for recipient in selected_recipients + custom_emails:
        email_address = RECIPIENTS.get(recipient, recipient)
        message = {
            "message": {
                "subject": f"Service Information Request - {location}",
                "body": {
                    "contentType": "Text",
                    "content": email_body
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": email_address
                        }
                    }
                ],
                "attachments": [
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": os.path.basename(attachment),
                        "contentType": "application/octet-stream",
                        "contentBytes": attachment_content
                    }
                ]
            }
        }

        # Send email using Microsoft Graph API
        response = requests.post(
            f"{GRAPH_ENDPOINT}/users/{SENDER_EMAIL}/sendMail",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json=message
        )

        if response.status_code == 202:
            st.success(f"Email sent successfully to {email_address}")
        else:
            st.error(f"Failed to send email to {email_address}. Status code: {response.status_code}")

def main():
    st.title("AECOM Service Information Request")

    # Get token
    token = get_token()
    if not token:
        st.error("Authentication failed. Please check your Azure AD configuration.")
        return

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
            preview = f"""To whom it may concern,

We are planning work in the {location} area. I have attached a location map to show where we would require service information. I would be obliged if you could provide me with details of any existing services at this location and within the surrounding area.

I trust you find this satisfactory, however if you should require any additional information or clarification, please do not hesitate to contact me at {return_email}.

Best regards,
{sender_name}"""
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
                
                send_email(token, sender_name, location, uploaded_file.name, return_email, selected_recipients, custom_email_list)
                
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
