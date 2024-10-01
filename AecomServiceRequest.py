import streamlit as st

# Recipient emails
RECIPIENTS = {
    "NIE": "Markups@nienetworks.co.uk",
    "Phoenix": "dialbeforeyoudig@phoenixnaturalgas.com",
    "Firmus": "dialb4udig@firmusenergy.co.uk",
    "Virgin Media": "PlantEnquiriesTeam@virginmedia.co.uk",
    "Northern DFI": "dfiroads.northern@infrastructure-ni.gov.uk",
    "Southern DFI": "dfiroads.southern@infrastructure-ni.gov.uk",
    "Eastern DFI": "dfiroads.eastern@infrastructure-ni.gov.uk",
    "Western DFI": "dfiroads.western@infrastructure-ni.gov.uk",
    "Greater Belfast Rivers": "rivers.belfast@infrastructure-ni.gov.uk",
    "Lisburn Rivers": "rivers.lisburn@infrastructure-ni.gov.uk",
    "Coleraine Rivers": "rivers.coleraine@infrastructure-ni.gov.uk",
    "Armagh Rivers": "rivers.armagh@infrastructure-ni.gov.uk",
    "Fermanagh Rivers": "rivers.fermanagh@infrastructure-ni.gov.uk",
    "Omagh Rivers": "rivers.omagh@infrastructure-ni.gov.uk",
    "Creator": "mark.kirkpatrick@aecom.com"
}


def generate_email(sender_name, location, return_email, recipients):
    recipient_emails = [RECIPIENTS.get(r, r) for r in recipients]
    to_line = "; ".join(recipient_emails)
    
    subject = f"Service Information Request - {location}"
    
    body = f"""To whom it may concern,

We are planning work in the {location} area. I have attached a location map to show where we would require service information. I would be obliged if you could provide me with details of any existing services at this location and within the surrounding area.

I trust you find this satisfactory, however if you should require any additional information or clarification, please do not hesitate to contact me at {return_email}.

Best regards,
{sender_name}

AECOM
"""
    
    full_email = f"To: {to_line}\nSubject: {subject}\n\n{body}"
    return full_email, to_line

def main():
    st.title("AECOM Service Information Request Email Generator")
    
    sender_name = st.text_input("Your Name")
    location = st.text_input("Work Location")
    return_email = st.text_input("Return Email Address")
    
    selected_recipients = st.multiselect("Select Recipients", options=list(RECIPIENTS.keys()))
    custom_emails = st.text_area("Custom Email Addresses (one per line)")
    
    st.warning("Remember to attach an image or document of the site boundary when sending the email!")
    
    if st.button("Generate Email"):
        if sender_name and location and return_email and (selected_recipients or custom_emails):
            custom_email_list = [email.strip() for email in custom_emails.split('\n') if email.strip()]
            all_recipients = selected_recipients + custom_email_list
            
            email_content, to_line = generate_email(sender_name, location, return_email, all_recipients)
            
            st.subheader("Generated Email:")
            st.text_area("Email Content:", email_content, height=400)
            
            col1, col2 = st.columns(2)
            with col1:
                st.text_area("Recipient Addresses:", to_line, height=100)
            with col2:
                st.markdown("### Copy buttons:")
                st.button("Copy Email Content", on_click=lambda: st.write(f'<p>{email_content}</p>', unsafe_allow_html=True))
                st.button("Copy Recipient Addresses", on_click=lambda: st.write(f'<p>{to_line}</p>', unsafe_allow_html=True))
            
            st.info("Don't forget to attach the site boundary image/document before sending the email!")
        else:
            st.warning("Please fill in all required fields and select at least one recipient.")
    
    st.markdown("---")
    st.markdown("Made by [Mark Kirkpatrick](mailto:mark.kirkpatrick@aecom.com)")
    st.markdown("For any queries, please email [mark.kirkpatrick@aecom.com](mailto:mark.kirkpatrick@aecom.com)")

if __name__ == "__main__":
    main()
