import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_gmail_message():
    # Load CSS
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found. Using default styles.")

    st.title("📧 GMail Message Sender")

    with st.expander("ℹ️ How to use GMail Message Sender", expanded=False):
        st.markdown("""
        **Features:**
        - Send a single email to a specified recipient.
        - Simple interface for quick emails.

        **How to use:**
        1. **Recipient Email**: Enter the email address of the person you want to send an email to.
        2. **Subject**: Enter the subject of your email.
        3. **Message**: Write the content of your email.
        4. **Gmail Credentials**: Enter your Gmail address and an App Password to send the email.

        **Security Note:** Use Gmail App Passwords for better security instead of your main password.
        """)

    recipient_email = st.text_input("Enter recipient's email address:", help="The email address of the person you want to send an email to (e.g., friend@example.com).")
    subject = st.text_input("Enter the subject of the email:", help="The subject line of your email.")
    message = st.text_area("Enter your message:", help="The main body of your email.")
    st.subheader("🔐 Gmail Credentials")
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("Enter your Gmail address:", value=None, help="Your Gmail address (e.g., example@gmail.com).")
    
    with col2:
        sender_password = st.text_input("Enter your Gmail app password:", value=None, type="password", 
                                      help="Use a Gmail App Password for better security. Do not use your regular password.")
    

    if st.button("📤 Send GMail Message", type="primary"):
        if recipient_email and subject and message and sender_email and sender_password:
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                server.quit()
                st.success(f"✅ Email sent to {recipient_email} with subject '{subject}'.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.write("💡 **Troubleshooting tips:**")
                st.write("- Make sure you're using an App Password, not your regular Gmail password")
                st.write("- Enable 2-factor authentication and generate an App Password")
                st.write("- Check if 'Less secure app access' is enabled (not recommended)")
        else:
            st.error("⚠️ Please fill in all fields.")
