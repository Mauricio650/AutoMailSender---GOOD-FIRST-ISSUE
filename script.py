import smtplib
import os
import pandas as pd
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Configure logging
logging.basicConfig(
    filename='email_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

sender_email = "YOUR EMAIL"
password = "YOUR PASSWORD"

def get_Client_Data(row):
    try:
        idClient = row['id']
        nameClient = row['name']
        addressEmailClient = row['email']
        return [idClient, nameClient, addressEmailClient]
    except Exception as e:
        logging.error(f"Error reading client data: {e}")
        return None

def Create_ServerConnection_And_Send_Mail(receiver_email, message, sender_email, password):
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        logging.info(f"Email sent successfully to: {receiver_email}")
    except Exception as e:
        logging.error(f"Failed to send email to {receiver_email}: {e}")

def Builder_Message(nameClient, idClient, addressEmailClient, sender_email):
    subject = "EMAIL SUBJECT"
    email_body = "EMAIL BODY"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = addressEmailClient
    message['Subject'] = subject
    message.attach(MIMEText(email_body, 'plain'))
    return message

def Attach_Files(message):
    pdfFilePaths = ["C:\\YOUR PATH"]

    for pdfPath in pdfFilePaths:
        try:
            fileName = os.path.basename(pdfPath)
            with open(pdfPath, 'rb') as file:
                part = MIMEApplication(file.read(), Name=fileName)
            part['Content-Disposition'] = f'attachment; filename="{fileName}"'
            message.attach(part)
        except Exception as e:
            logging.error(f"Error attaching file {pdfPath}: {e}")

def Send_Email(getClientData, BuilderMessage, AttachFiles, CreateServerConnection):
    try:
        df = pd.read_excel("./Libro.xlsx")
        
        for index, row in df.iterrows():
            arrayData = getClientData(row)
            
            if arrayData is None:
                continue
                
            try:
                if isinstance(arrayData[2], float):
                    logging.warning(f"No email for client {arrayData[1]} (ID: {arrayData[0]})")
                    continue
                    
                message = BuilderMessage(arrayData[1], arrayData[0], arrayData[2], sender_email)
                AttachFiles(message)
                CreateServerConnection(arrayData[2], message, sender_email, password)
                
            except Exception as e:
                logging.error(f"Error processing email for {arrayData[1]} (ID: {arrayData[0]}): {e}")
                continue
                
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
    finally:
        logging.info("Finished sending all emails.")

# Run main
Send_Email(get_Client_Data, Builder_Message, Attach_Files, Create_ServerConnection_And_Send_Mail)
