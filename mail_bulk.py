import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import time

def send_gmail_bulk_message():
    # Load CSS
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found. Using default styles.")

    st.title("📧 Gmail Bulk Message Sender")
    
    # Navigation info
    st.markdown("""
    <div style="background-color: #1e2329; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h4 style="color: #00aaff; margin-top: 0;">📍 Navigation Guide</h4>
        <p style="margin-bottom: 5px;"><strong>Step 1:</strong> 🔐 Enter your Gmail credentials</p>
        <p style="margin-bottom: 5px;"><strong>Step 2:</strong> 📁 Upload your CSV file and email template</p>
        <p style="margin-bottom: 5px;"><strong>Step 3:</strong> 📝 Map your CSV columns to template variables</p>
        <p style="margin-bottom: 5px;"><strong>Step 4:</strong> 📋 Preview your email and send bulk messages</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Help and instructions
    with st.expander("ℹ️ Complete Guide - How to use Gmail Bulk Message Sender", expanded=False):
        st.markdown("""
        ## 🚀 Features
        - Send personalized emails to multiple recipients (up to 500 at once)
        - Support for CSV, XLSX, XLS, and TSV file uploads
        - Advanced email templating with personalization variables
        - Subject line personalization with dynamic content
        - File attachments support (PDF, DOCX, images, etc.)
        - Real-time sending progress with detailed status updates
        - Error handling and detailed reporting
        
        ## 📋 Step-by-Step Instructions
        
        ### 1. Prepare Your Files
        **CSV/Excel File Requirements:**
        - Must contain an email column (automatically detected)
        - Additional columns for personalization (name, company, date, etc.)
        - Maximum 500 rows for bulk sending
        - Supported formats: CSV, XLSX, XLS, TSV
        
        **Template File (.txt):**
        - Plain text file with your email content
        - Use curly braces for variables: `{variable_name}`
        - Example: "Hello {name}, your appointment with {company} is on {date}"
        
        ### 2. CSV File Example
        ```
        email,name,company,appointment_date,location
        john@example.com,John Doe,ABC Corp,2025-07-01,New York
        jane@example.com,Jane Smith,XYZ Ltd,2025-07-02,Boston
        ```
        
        ### 3. Template Example
        ```
        Hello {name},
        
        Thank you for scheduling an appointment with {company}.
        
        Your appointment details:
        - Date: {appointment_date}
        - Location: {location}
        
        Please let us know if you need to reschedule.
        
        Best regards,
        Your Team
        ```
        
        ### 4. Subject Line Example
        ```
        Appointment Confirmation for {name} - {appointment_date}
        ```
        
        ## 🔒 Security Best Practices
        - **Never use your regular Gmail password**
        - Enable 2-Factor Authentication on your Gmail account
        - Generate and use Gmail App Passwords
        - Keep your credentials secure and don't share them
        
        ## 📧 Gmail App Password Setup
        1. Go to your Google Account settings
        2. Navigate to Security → 2-Step Verification
        3. Select App passwords
        4. Generate a new app password for "Mail"
        5. Use this 16-character password in the app
        
        ## ⚠️ Important Notes
        - Test with a small batch first (2-3 emails)
        - Respect email sending limits to avoid being flagged as spam
        - Ensure all recipients have consented to receive emails
        - Double-check your template for typos before sending
        """)    
    # Gmail credentials section
    st.markdown("---")
    st.subheader("🔐 Step 1: Gmail Credentials")
    st.info("💡 **Security Tip:** Always use Gmail App Passwords instead of your regular password for better security!")
    
    with st.expander("🔒 How to get Gmail App Password", expanded=False):
        st.markdown("""
        **Follow these steps to create a Gmail App Password:**
        1. Go to your Google Account settings (myaccount.google.com)
        2. Click on "Security" in the left sidebar
        3. Under "Signing in to Google", click "2-Step Verification" (enable if not already)
        4. Scroll down and click "App passwords"
        5. Select "Mail" as the app and generate password
        6. Copy the 16-character password and use it below
        
        **Note:** You must have 2-Factor Authentication enabled to create App Passwords.
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sender_email = st.text_input("Enter your Gmail address:", value=None, help="Your Gmail address (e.g., example@gmail.com)")
    
    with col2:
        sender_password = st.text_input("Enter your Gmail app password:", value=None, type="password", 
                                      help="Use a Gmail App Password for better security. Do not use your regular password.")    
    if not sender_email or not sender_password:
        st.error("⚠️ Please enter valid Gmail credentials to proceed")
        
    # File upload section
    st.markdown("---")
    st.subheader("📁 Step 2: Upload Your Files")
    st.info("📝 **Required:** CSV file with recipient data and TXT template file. **Optional:** Attachment files.")
    
    with st.expander("📋 File Requirements & Examples", expanded=False):
        st.markdown("""
        ### CSV File Requirements:
        - **Must have:** Email column (will be auto-detected)
        - **Can have:** Any additional columns for personalization
        - **Formats:** CSV, XLSX, XLS, TSV
        - **Limit:** Maximum 500 rows
        
        ### Template File Requirements:
        - **Format:** Plain text (.txt) file only
        - **Variables:** Use {column_name} for personalization
        - **Example:** "Hello {name}, your order #{order_id} is ready!"
        
        ### Attachment Files:
        - **Optional:** Add files to send with every email
        - **Formats:** Any file type (PDF, DOCX, images, etc.)
        - **Note:** Same attachments will be sent to all recipients
        """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        file = st.file_uploader(
            "📊 Upload CSV file",
            type=["csv", "xlsx","xls","tsv"],
            accept_multiple_files=False,
            help="Upload a CSV, XLSX, XLS, or TSV file containing recipient emails and other data for personalization."
        )
        
    with col2:
        template = st.file_uploader(
            "📝 Upload email template",
            type=["txt"],
            accept_multiple_files=False,
            help="Upload a text file (.txt) containing your email template. You can use {fieldname} for personalization (e.g., 'Hello {name}')."
        )
    with col3:
        uploaddata = st.file_uploader(
            "📄 Upload additional data file",
            help= "Upload any files you want to send as attachments to all recipients (e.g., PDF, DOCX, images).",
            accept_multiple_files=True
        )    
    # Subject line input
    st.markdown("---")
    st.subheader("📝 Step 3: Email Subject Line")
    st.info("💡 **Tip:** Use {variable_name} to personalize subject lines just like in your template!")
    
    subject = st.text_input("Enter the subject of the email:", 
                           help="You can use {fieldname} for personalization. For example: 'Meeting Confirmation for {name} - {date}'.",
                           placeholder="e.g., Hello {name}, your appointment is confirmed!")
    
    st.success("🎯 **Pro Tips for Better Email Delivery:**")
    st.markdown("""
    - Keep subject lines under 50 characters for better mobile display
    - Avoid spam trigger words like 'FREE', 'URGENT', excessive exclamation marks
    - Personalize subject lines to improve open rates
    - Test your emails with a small batch first
    """)
    
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
            
        st.markdown("---")
        st.subheader("📊 Step 4: Data Preview & Configuration")
        st.success(f"✅ Successfully loaded {len(filedata)} rows from your file!")
        
        with st.expander("📋 View Your Data (First 7 rows)", expanded=False):
            st.dataframe(filedata.head(7))
            
        st.info(f"📈 **Data Summary:** {len(filedata)} total rows • {len(filedata.columns)} columns detected")
        
        columns = filedata.columns.tolist()
        memo = {}
        
        # Email column selection
        st.markdown("### 📧 Email Column Selection")
        emailcolumnopts = [
            'mail', 'gmail', 'email', 'g-mail', 'e-mail', 'e mail', 'email Address', 'e-mail Address', 'g mail',
            'recipient', 'to', 'receiver','user', 'address', 
        ]
        for a in columns:
            if a.lower() in emailcolumnopts:
                emailcolumn = a
                break
         # Default to first column if no email column found
            
        emailcolumn = st.selectbox("Select the column containing email addresses", 
                                 options=columns, 
                                 index=columns.index(emailcolumn), 
                                 help="Choose the column from your uploaded file that contains the recipient email addresses.")
        
        st.markdown("---")
        st.subheader("📝 Step 5: Column Mapping for Personalization")
        st.info("🎯 **Map your CSV columns to template variables.** Leave empty for columns you don't want to use.")
        
        with st.expander("� How Column Mapping Works", expanded=False):
            st.markdown("""
            **What is Column Mapping?**
            This step connects your CSV columns to variables in your email template.
            
            **Example:**
            - If your CSV has a column called "customer_name"
            - You can map it to template variable "name"
            - Then use {name} in your template
            - The system will replace {name} with actual customer names
            
            **Benefits:**
            - Clean template variables (use "name" instead of "customer_name_with_underscores")
            - Flexibility to reuse templates with different CSV formats
            - Skip columns you don't need in emails            """)
        
        for i in range(len(columns)):
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown(f"**Column:** `{columns[i]}`")
                st.dataframe(filedata[columns[i]].head(2), use_container_width=True)
                
            with col2:
                text = st.text_input(f"Template variable name for '{columns[i]}' (leave empty to skip)", 
                                   value=columns[i],
                                   help=f"Enter a variable name to use in your template as {{{columns[i]}}}. Example: if you enter 'name', use {{name}} in your template.",
                                   key=f"col_{i}")
                                   
            st.markdown("---")
            if text.strip():
                memo[columns[i]] = text.strip()

        filedata = filedata.dropna(subset=[emailcolumn])  # Ensure email column exists and is not empty
        filedata = filedata[filedata[emailcolumn].str.contains('@', na=False)]  # Filter rows with valid email format
        
        # Data validation
        if len(filedata) == 0:
            st.error("❌ No valid email addresses found in your file. Please check your data.")
            return
        elif len(filedata) > 500:
            st.error("⚠️ The number of valid email rows must be less than 500. Please reduce your data size.")
            return
        else:
            st.success(f"✅ Found {len(filedata)} valid email addresses ready for sending!")
            
    else:
        st.error("📁 Please upload a CSV file with recipient emails to continue.")
        return
    
    # Template processing
    st.markdown("---")
    st.subheader("📋 Step 6: Email Preview & Validation")
    
    if template is not None:
        message_template = template.read().decode('utf-8')
        
        if filedata is not None and len(filedata) > 0:
            st.info("� **Preview shows how your first email will look.** All emails will be personalized similarly.")
            
            # Generate preview using first row
            personalized_message = message_template
            personalized_subject = subject
            row = filedata.iloc[0]  
            
            if template is not None:
                for csv_col, template_var in memo.items():
                    if template_var and csv_col in row:
                        personalized_message = personalized_message.replace(f'{{{template_var}}}', str(row[csv_col]))
                        personalized_subject = personalized_subject.replace(f'{{{template_var}}}', str(row[csv_col]))
                
                with st.container():
                    st.markdown("### 📧 Email Preview")
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("**Email Details:**")
                        st.write(f"**📧 To:** {row[emailcolumn]}")
                        st.write(f"**📝 Subject:** {personalized_subject}")
                        st.write(f"**📊 Total Recipients:** {len(filedata)}")
                        if uploaddata:
                            st.write(f"**📎 Attachments:** {len(uploaddata)} file(s)")
                    
                    with col2:
                        st.markdown("**Message Content:**")
                        st.text_area("Preview:", value=personalized_message, height=200, disabled=True)
                        
                # Variables used summary
                used_vars = [var for var in memo.values() if var and f'{{{var}}}' in message_template]
                if used_vars:
                    st.success(f"🎯 **Template Variables Found:** {', '.join(used_vars)}")
                else:
                    st.warning("⚠️ **No template variables detected.** Your emails will be identical for all recipients.")
                    
    else:
        st.error("📝 Please upload a template file to continue.")
        return
    
    # Final sending section
    st.markdown("---")
    st.subheader("🚀 Step 7: Send Bulk Emails")
    
    with st.expander("⚠️ Important - Read Before Sending", expanded=False):
        st.markdown("""
        ### 🛡️ Safety Checklist:
        - [ ] **Test first:** Send to yourself or a small group initially
        - [ ] **Double-check recipients:** Ensure all email addresses are correct
        - [ ] **Review content:** Check for typos and proper personalization
        - [ ] **Verify attachments:** Make sure attached files are correct
        - [ ] **Respect limits:** Don't exceed Gmail's sending limits (500/day recommended)
        
        ### 📊 What happens when you click Send:
        1. **Connection:** App connects to Gmail using your credentials
        2. **Processing:** Each email is personalized and prepared
        3. **Sending:** Emails are sent one by one with progress updates
        4. **Reporting:** You'll get a detailed summary of results
        
        ### ⏱️ Estimated Time:
        - Small batch (1-50 emails): 1-2 minutes
        - Medium batch (51-200 emails): 3-5 minutes  
        - Large batch (201-500 emails): 8-12 minutes
        """)
    
    if st.button("📤 Send Gmail Bulk Messages", type="primary", help="Click to start sending emails to all recipients"):
        starttime = time.time()
        
        # Validate inputs
        if not sender_email or not sender_password:
            st.error("⚠️ Please enter your Gmail credentials.")
            return
        
        if not subject or not message_template:
            st.error("⚠️ Please provide both subject and message template.")
            return
          # Progress tracking
        status_text = st.empty()
        result_container = st.container()
        
        # Show initial status
        status_text.info("🔄 Preparing to send emails...")
        
        parts = []
        if uploaddata is not None:
            status_text.info("📎 Processing attachments...")
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
            status_text.info("🔗 Connecting to Gmail server...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            status_text.success("✅ Successfully connected to Gmail!")
            time.sleep(1)
            
            # Initialize progress tracking
            total_emails = len(filedata)
            successful_sends = 0
            failed_sends = 0
            
            # Send emails
            status_text.info(f"📤 Starting to send {total_emails} emails...")
            
            for index, row in filedata.iterrows():
                recipient_email = row[emailcolumn]
                
                # Update status for current email
                status_text.info(f"📧 Sending email {index + 1}/{total_emails} to {recipient_email}")
                
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
                    
                    # Add attachments
                    for part in parts:
                        msg.attach(part)
                    
                    # Send email
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    successful_sends += 1
                    
                    # Brief pause to avoid overwhelming the server
                    time.sleep(0.1)
                    
                except Exception as e:
                    failed_sends += 1
                    with result_container:
                        st.error(f"❌ Failed to send email to {recipient_email}: {str(e)}")
            
            # Final status
            status_text.success(f"🎉 Email sending completed! ✅ {successful_sends} sent, ❌ {failed_sends} failed")            
            server.quit()
            endtime = time.time()
            
            # Final results
            st.success(f"🎉 Bulk email sending completed!")
            st.info(f"📊 **Results Summary:**\n"
                   f"- Total emails attempted: {successful_sends + failed_sends}\n"
                   f"- Successfully sent: {successful_sends}\n"
                   f"- Errors: {failed_sends}\n"
                   f"- Time taken: {endtime - starttime:.2f} seconds")
            
        except Exception as e:
            st.error(f"❌ Error connecting to Gmail: {e}")
            st.write("💡 **Troubleshooting tips:**")
            st.write("- Make sure you're using an App Password, not your regular Gmail password")
            st.write("- Enable 2-factor authentication and generate an App Password")
            st.write("- Check if 'Less secure app access' is enabled (not recommended)")
            if 'server' in locals():
                server.quit()