import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



sender_email = "YOUR EMAIL" 
password = "YOUR PASSWORD"

def get_Client_Data(initialCounter):
    
    df = pd.read_excel("C:\\your_path") # download the excel in the repository and try
    
    idClient  = df.values[initialCounter][0]     # [0]<-- columns position
    nameClient = df.values[initialCounter][1] # [initialCounter]<-- row position
    addressEmailClient = df.values[initialCounter][2]
    
    return [idClient, nameClient, addressEmailClient]

def Create_ServerConnection_And_Send_Mail(receiver_email, message, sender_email, password):
    # sender
    sender_email = sender_email
    password = password

    #server configuration SMTP
    smtp_server = 'smtp.office365.com' #(gmail = 'smtp.gmail.com') YOU MUST TO CHANGE THE SERVER IS YOUR EMAIL IS NOT OUTLOOK - SEARCH YOUR SMTP SERVER ON CHAT GPT
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls() # start the safe TLS connection
        server.login(sender_email, password) # LOG IN
        server.sendmail(sender_email, receiver_email, message.as_string()) # SEND DE EMAIL

def Builder_Message(nameClient,idClient,addressEmailClient,sender_email):
    #body and subject
    subject = "EMAIL SUBJECT" 
    email_body = "EMAIL BODY"

    # message builder
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = addressEmailClient
    message['Subject'] = subject

    message.attach(MIMEText(email_body,'plain'))
    return message

def Attach_Files(message):

    # PATHS OF YOUR ATTACH FILES IF THERE ARE TWO OR MORE
    pdfFilePaths = ["C:\\YOUR PATH"]
    
    for pdfPath in pdfFilePaths:
        fileName = os.path.basename(pdfPath) # NAME OF YOUR ATTACH FILE
        
        with open(pdfPath, 'rb') as file:  # INSERT THE FILES IN THE EMAIL
            part = MIMEApplication(file.read(), Name=fileName)
        part['Content-Disposition'] = f'attachment; filename="{fileName}"'
        message.attach(part) 



# MAIN FUNCTION
def Send_Email(getClientData, BuilderMessage, AttachFiles, CreateServerConnection):


    for initialCounter in range(0,2): # NUMBER OF ROWS IN YOUR EXCEL
        #Extract the user data in the excel [data1, data2, data3, ..., ...]
        arrayData = get_Client_Data(initialCounter)

        
        # THIS CONDITION CAN BE UTIL IF YOU NEEDED VALIDATE SOMEONE DATA BEFORE SEND YHE MAIL
        if type(arrayData[2]) == float:
            # READ THE EXCEL
            df = pd.read_excel("C:\\PATH of your excel")

            # create new row with a dataframe
            new_row= pd.DataFrame({'DataUser': [arrayData[1]], 'DataUser2': [arrayData[0]]}) #name of columns and data

            # Concatenate existing DataFrame with new row
            df = pd.concat([df, new_row], ignore_index=True)

            # save the updated dataframe
            df.to_excel("C:\\PATH of your excel", index=False)
        else:
            
            message = Builder_Message(arrayData[1],arrayData[0],arrayData[2],sender_email)
            Attach_Files(message)
            Create_ServerConnection_And_Send_Mail(arrayData[2],message)
            print('MAIL SENT :', arrayData[1])

    return print('--------------------THE MAILS WERE SENT SUCCESSFULLY------------------')




# main function
Send_Email(get_Client_Data, Builder_Message, Attach_Files, Create_ServerConnection_And_Send_Mail)































