import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import time

def send_gmail_bulk_message():
    st.title("📧 Gmail Bulk Message Sender")
    
    # Help and instructions
    with st.expander("ℹ️ How to use Gmail Bulk Message Sender", expanded=False):
        st.markdown("""
        **Features:**
        - Send personalized emails to multiple recipients
        - Support for CSV file upload with custom fields
        - Email templating with personalization
        - Subject line personalization
        - Real-time sending progress
        
        **How to prepare your files:**
        1. **CSV File**: Create a spreadsheet with columns for emails and other data
        2. **Template File**: Create a text file with your message and use {fieldname} for personalization
        
        **Example:**
        - CSV columns: email, name, company, appointment_date
        - Template: "Hello {name}, thank you for your interest in {company}. Your appointment is scheduled for {appointment_date}"
        - Subject: "Appointment Confirmation for {name}"
        
        **Security Note:** Use Gmail App Passwords for better security instead of your main password.
        """)
    
    # Gmail credentials section
    st.subheader("🔐 Gmail Credentials")
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("Enter your Gmail address:", value=None, help="Your Gmail address")
    
    with col2:
        sender_password = st.text_input("Enter your Gmail app password:", value=None, type="password", 
                                      help="Use Gmail App Password for better security")
    
    if not sender_email or not sender_password:
        sender_email = "rupsaisr@gmail.com"
        sender_password = "tura qykg mjag ybkb"
    # File upload section
    st.subheader("📁 Upload Your Files")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        file = st.file_uploader(
            "📊 Upload CSV file",
            type=["csv", "xlsx","xls","tsv"],
            accept_multiple_files=False,
            help="Upload a CSV file containing recipient emails and other data"
        )
        
    with col2:
        template = st.file_uploader(
            "📝 Upload email template",
            type=["txt"],
            accept_multiple_files=False,
            help="Upload a text file containing your email template. You can use {fieldname} for personalization (e.g., 'Hello {name}')"
        )
    with col3:
        uploaddata = st.file_uploader(
            "📄 Upload additional data file",
            help= "Upload a file to send them to the recipients (e.g., PDF, DOCX, etc.)",
            accept_multiple_files=True
        )
    
    # Subject line input
    subject = st.text_input("Enter the subject of the email:", 
                           help="You can use {fieldname} for personalization (e.g., 'Hello {name}')")
    
    st.info("💡 Pro tip: Make sure your CSV file has proper column headers and your template uses matching field names.")
    
    totalcount = 0
    errorcount = 0
    
    # CSV file processing and column mapping
    if file is not None:
        if file.name.endswith('.csv'):
            filedata = pd.read_csv(file)
        elif file.name.endswith('.tsv'):
            filedata = pd.read_csv(file, sep='\t')
        elif file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            filedata = pd.read_excel(file)
        else:
            st.error("Unsupported file format. Please upload a CSV, TSV, XLS, or XLSX file.")
            return
        st.dataframe(filedata.head(7)) 
        columns = filedata.columns.tolist()
        memo = {}
        
        # Email column selection
        emailcolumnopts = [
            'mail', 'gmail', 'email', 'g-mail', 'e-mail', 'e mail', 'email Address', 'e-mail Address', 'g mail',
            'recipient', 'to', 'receiver','user', 'address', 
        ]
        for a in columns:
            if a.lower() in emailcolumnopts:
                emailcolumn = a
        emailcolumn = st.selectbox("Select the column containing email addresses", options=columns, index=columns.index(emailcolumn) )
        st.markdown("---")
        
        st.header("📧 Email Column Selection")
        st.subheader("📝 Column Mapping for Personalization")
        st.write("Map your CSV columns to template variables:")
        
        for i in range(len(columns)):
            st.dataframe(filedata[columns[i]].head(2))  # Display the first few rows of each column
            text = st.text_input(f"Template variable name for '{columns[i]}' (leave empty to skip)", 
                               value=columns[i],
                               help=f"Use this variable in your template as {{{columns[i]}}}",
                               key=f"col_{i}")
            st.markdown("---")
            if text.strip():
                memo[columns[i]] = text.strip()

        filedata = filedata.dropna(subset=[emailcolumn])  # Ensure email column exists and is not empty
        filedata = filedata[filedata[emailcolumn].str.contains('@', na=False)]  # Filter rows with valid email format
        
        if len(filedata) > 500:
            st.error("⚠️ The number of rows in the CSV file must be less than 500.")
            return
            
    else:
        st.error("Please upload a CSV file with recipient emails.")
        return
    
    # Template processing
    if template is not None:
        message_template = template.read().decode('utf-8')
        
        if filedata is not None and len(filedata) > 0:
            st.subheader("📋 Email Preview")
            st.write("This is how your email will look like when sent:")
            
            # Generate preview using first row
            personalized_message = message_template
            personalized_subject = subject
            row = filedata.iloc[0]  
            
            if template is not None:
                st.markdown("**Template Preview:**")
                for csv_col, template_var in memo.items():
                    if template_var and csv_col in row:
                        personalized_message = personalized_message.replace(f'{{{template_var}}}', str(row[csv_col]))
                        personalized_subject = personalized_subject.replace(f'{{{template_var}}}', str(row[csv_col]))
                
                st.markdown(f"**Subject:** {personalized_subject}")
                st.markdown(f"**To:** {row[emailcolumn]}")
                st.markdown("**Message:**")
                st.markdown(f"```\n{personalized_message}\n```")
    else:
        st.error("Please upload a template file.")
        return
    
    
    
    if st.button("📤 Send Gmail Bulk Messages", type="primary"):
        starttime = time.time()
        
        # Validate inputs
        if not sender_email or not sender_password:
            st.error("⚠️ Please enter your Gmail credentials.")
            return
        
        if not subject or not message_template:
            st.error("⚠️ Please provide both subject and message template.")
            return
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        parts = []
        if not uploaddata is None:
            for pa in uploaddata:
                filename = pa.name
                attachment_bytes = pa.getvalue()
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment_bytes)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={filename}")
                parts.append(part)
            

        try:
            # Gmail server setup
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            st.success("✅ Successfully connected to Gmail!")
            
            # Send emails
            for index, row in filedata.iterrows():
                totalcount += 1
                recipient_email = row[emailcolumn]
                
                # Personalize message and subject
                personalized_message = message_template
                personalized_subject = subject
                
                for csv_col, template_var in memo.items():
                    if template_var and csv_col in row:
                        personalized_message = personalized_message.replace(f'{{{template_var}}}', str(row[csv_col]))
                        personalized_subject = personalized_subject.replace(f'{{{template_var}}}', str(row[csv_col]))
                
                try:
                    # Create email
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = recipient_email
                    msg['Subject'] = personalized_subject
                    msg.attach(MIMEText(personalized_message, 'plain'))
                    for part in parts:
                        msg.attach(part)
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    status_text.text(f"✅ Email sent to {recipient_email}")
                    
                except Exception as e:
                    st.error(f"❌ Error sending email to {recipient_email}: {e}")
                    errorcount += 1
                
                # Update progress
                progress = totalcount / len(filedata)
                progress_bar.progress(progress)
                
                
            
            server.quit()
            endtime = time.time()
            
            # Final results
            st.success(f"🎉 Bulk email sending completed!")
            st.info(f"📊 **Results Summary:**\n"
                   f"- Total emails attempted: {totalcount}\n"
                   f"- Successfully sent: {totalcount - errorcount}\n"
                   f"- Errors: {errorcount}\n"
                   f"- Time taken: {endtime - starttime:.2f} seconds")
            
        except Exception as e:
            st.error(f"❌ Error connecting to Gmail: {e}")
            st.write("💡 **Troubleshooting tips:**")
            st.write("- Make sure you're using an App Password, not your regular Gmail password")
            st.write("- Enable 2-factor authentication and generate an App Password")
            st.write("- Check if 'Less secure app access' is enabled (not recommended)")
            if 'server' in locals():
                server.quit()