import streamlit as st
from mail import send_gmail_message 
from mail_bulk import send_gmail_bulk_message

st.set_page_config(
    page_title="WhatsApp Message Sender",
    page_icon="📱",
    layout="centered"
)

st.sidebar.title("Select your application")
app = st.sidebar.selectbox(
    "Select Application",
    options=["GMail","GmailBulk"],
    index=1
)

# Add sidebar with instructions
with st.sidebar:
        st.header("📋 Instructions")
        st.write("""
        1. **Configure Gmail credentials** in your application
        2. **Enter recipient email addresses** (single or multiple)
        3. **Write your subject line** and message content
        4. **Review your message** before sending
        5. **Click Send** to deliver your emails
        
        **Important:**
        - Ensure Gmail account has app passwords enabled
        - Use valid email addresses
        - Check spam folder if emails don't arrive
        """)

        st.header("🔧 Troubleshooting")
        st.write("""
        **Common Issues:**
        - Gmail authentication failed
        - Invalid email address format
        - App password not configured
        - SMTP connection blocked
        - Internet connection issues
        """)
    



if app == "GMail":
    send_gmail_message()

elif app == "GmailBulk":
    send_gmail_bulk_message()