# Gmail Bulk Message Sender

This project is a Gmail Bulk Message Sender application that allows users to send personalized emails to multiple recipients using a CSV file for recipient data and a text file for email templates.

## Features

- Send personalized emails to multiple recipients
- Support for CSV file upload with custom fields
- Email templating with personalization
- Subject line personalization
- Real-time sending progress

## How to Use

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd mailproject
   ```

2. **Install dependencies**:
   Make sure you have Python installed. Then, install the required libraries using pip:
   ```
   pip install -r requirements.txt
   ```

3. **Prepare your files**:
   - **CSV File**: Create a spreadsheet with columns for emails and other data.
   - **Template File**: Create a text file with your message and use `{fieldname}` for personalization.

   **Example**:
   - CSV columns: `email`, `name`, `company`, `appointment_date`
   - Template: `"Hello {name}, thank you for your interest in {company}. Your appointment is scheduled for {appointment_date}"`
   - Subject: `"Appointment Confirmation for {name}"`

4. **Run the application**:
   Launch the application using Streamlit:
   ```
   streamlit run mail_bulk.py
   ```

5. **Enter your Gmail credentials**:
   Use your Gmail address and an App Password for better security.

6. **Upload your files**:
   Upload the CSV file with recipient data and the text file with your email template.

7. **Send emails**:
   Click the "Send Gmail Bulk Messages" button to start sending personalized emails.

## Security Note

For better security, use Gmail App Passwords instead of your main password. Make sure to enable 2-factor authentication on your Google account.

## License

This project is open-source and available under the MIT License.