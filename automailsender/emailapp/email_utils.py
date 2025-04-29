import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.conf import settings
import tempfile


def create_server_connection_and_send_mail(receiver_email, message, sender_email, password):
    """Establish SMTP connection and send email"""
    smtp_server = 'smtp.office365.com'  # Change as needed
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # start the safe TLS connection
        server.login(sender_email, password)  # LOG IN
        server.sendmail(sender_email, receiver_email, message.as_string())  # SEND THE EMAIL


def build_message(sender_email, recipient_email, subject, body):
    """Build email message with subject and body"""
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))
    return message


def attach_files(message, attachment_files):
    """Attach files to the email message"""
    if attachment_files:
        for attachment in attachment_files:
            # Get the file name
            file_name = os.path.basename(attachment.name)
            
            # Attach the file
            part = MIMEApplication(attachment.read(), Name=file_name)
            part['Content-Disposition'] = f'attachment; filename="{file_name}"'
            message.attach(part)


def send_single_email(sender_email, password, recipient_email, subject, body, attachment_files=None):
    """Send a single email with optional attachments"""
    try:
        # Build the message
        message = build_message(sender_email, recipient_email, subject, body)
        
        # Attach files if provided
        if attachment_files:
            attach_files(message, attachment_files)
        
        # Send the email
        create_server_connection_and_send_mail(recipient_email, message, sender_email, password)
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"


def send_bulk_emails(sender_email, password, excel_file, subject, body, attachment_files=None):
    """Send emails to multiple recipients from an Excel file"""
    results = []
    try:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            for chunk in excel_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        # Read the Excel file
        df = pd.read_excel(temp_file_path)
        os.unlink(temp_file_path)  # Delete the temporary file
        
        # Process each row
        for index, row in df.iterrows():
            try:
                # Extract client data
                client_id = row.iloc[0]  # First column: Client ID
                client_name = row.iloc[1]  # Second column: Client Name
                client_email = row.iloc[2]  # Third column: Client Email
                
                # Skip if email is missing or invalid
                if pd.isna(client_email) or not isinstance(client_email, str):
                    results.append({
                        "client_name": client_name,
                        "client_id": client_id,
                        "status": "Skipped",
                        "message": "Invalid or missing email address"
                    })
                    continue
                
                # Personalize the message with client's name
                personalized_body = body.replace("{client_name}", client_name)
                personalized_body = personalized_body.replace("{client_id}", str(client_id))
                
                # Build the email message
                message = build_message(sender_email, client_email, subject, personalized_body)
                
                # Attach files if provided
                if attachment_files:
                    # Reset file pointers for each email
                    for attachment in attachment_files:
                        attachment.seek(0)
                    attach_files(message, attachment_files)
                
                # Send the email
                create_server_connection_and_send_mail(client_email, message, sender_email, password)
                
                results.append({
                    "client_name": client_name,
                    "client_id": client_id,
                    "status": "Success",
                    "message": f"Email sent to {client_email}"
                })
            except Exception as e:
                results.append({
                    "client_name": row.iloc[1] if len(row) > 1 else "Unknown",
                    "client_id": row.iloc[0] if len(row) > 0 else "Unknown",
                    "status": "Failed",
                    "message": f"Error: {str(e)}"
                })
        
        return True, results
    except Exception as e:
        return False, f"Error processing bulk emails: {str(e)}"