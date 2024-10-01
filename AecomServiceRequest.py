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
    return full_email, to_line, body

def main():
    st.set_page_config(page_title="AECOM Email Generator", page_icon="📧", layout="wide")
    
    st.title("📧 AECOM Service Information Request Email Generator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Email Details")
        sender_name = st.text_input("👤 Your Name")
        location = st.text_input("📍 Work Location")
        return_email = st.text_input("📮 Return Email Address")
        
        st.subheader("🎯 Recipients")
        selected_recipients = st.multiselect("Select Recipients", options=list(RECIPIENTS.keys()))
        
        with st.expander("➕ Add Custom Email Addresses"):
            custom_emails = st.text_area("Enter one email per line")
    
    with col2:
        st.subheader("📎 Attachments")
        st.warning("⚠️ Remember to attach an image or document of the site boundary when sending the email!")
        
        st.subheader("🔍 Preview")
        if sender_name and location and return_email and (selected_recipients or custom_emails):
            custom_email_list = [email.strip() for email in custom_emails.split('\n') if email.strip()]
            all_recipients = selected_recipients + custom_email_list
            
            email_content, to_line, body = generate_email(sender_name, location, return_email, all_recipients)
            
            st.markdown(f"**To:** {to_line}")
            st.markdown(f"**Subject:** Service Information Request - {location}")
            st.markdown(body)
            
            st.info(f"📊 Character count: {len(body)}")
        else:
            st.info("Fill in the details to see a preview of your email here.")
    
    if st.button("🚀 Generate Email"):
        if sender_name and location and return_email and (selected_recipients or custom_emails):
            st.success("Email generated successfully!")
            st.text_area("📤 Generated Email Content", email_content, height=300)
        else:
            st.error("Please fill in all required fields and select at least one recipient.")
    
    st.markdown("---")
    st.markdown("Made with ❤️ by [Mark Kirkpatrick](mailto:mark.kirkpatrick@aecom.com)")
    st.markdown("For any queries, please email [mark.kirkpatrick@aecom.com](mailto:mark.kirkpatrick@aecom.com)")

if __name__ == "__main__":
    main()
