# 📧 AutoMailSender

This project is an automation tool for sending bulk emails to a list of clients defined in an Excel file. It is ideal for administrative tasks, reminders, notifications, or any email flow that needs to be personalized.

**🆕 NEW: Web Interface Available!** - Now includes a Django-based web interface for easier email management through your browser.

---

## 🚀 Features

### Core Features
- ✅ Load client data from an Excel file (`.xlsx`)
- ✅ Automatically generate a personalized message for each client
- ✅ Attach files to emails
- ✅ Use SMTP (compatible with Outlook, Gmail, etc.)
- ✅ Validate emails before sending
- ✅ Modular structure, easy to maintain

### 🌐 New Web Interface Features
- ✅ **User-friendly web interface** - No more command line needed!
- ✅ **Email settings management** - Configure SMTP settings through a web form
- ✅ **Single email sending** - Send individual emails with attachments
- ✅ **Bulk email management** - Upload Excel files and send to multiple recipients
- ✅ **Email personalization** - Use placeholders like `{client_name}` and `{client_id}`
- ✅ **Email logging and tracking** - View history of all sent emails
- ✅ **File attachment support** - Attach multiple files to single or bulk emails
- ✅ **Responsive design** - Works on desktop, tablet, and mobile devices
- ✅ **Real-time feedback** - See sending progress and results instantly
- ✅ **Error handling** - Clear error messages and troubleshooting guidance

---

## 🛠️ Requirements

- Python 3.10 or higher
- Python packages: `pandas`, `openpyxl`, `django` (for web interface)

Install them by running:

### For Console Script Only:
```bash
pip install pandas openpyxl
```

### For Web Interface:
```bash
pip install django pandas openpyxl
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

---

## 🧩 Project Structure

```
📂 AutoMailSender/
├── script.py                    # Original console script
├── README.md                    # This documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
└── automailsender/             # Django web application
    ├── manage.py               # Django management script
    ├── automailsender/         # Main Django project
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── emailapp/               # Email application
    │   ├── models.py           # Database models
    │   ├── views.py            # Web views
    │   ├── forms.py            # Web forms
    │   ├── email_utils.py      # Email sending logic
    │   └── urls.py             # URL routing
    └── templates/              # HTML templates
        └── emailapp/
            ├── base.html
            ├── home.html
            ├── settings.html
            ├── send_email.html
            ├── bulk_email.html
            ├── bulk_results.html
            └── logs.html
```

---

## 📋 Excel File Format

For bulk emails, your Excel file should have at least three columns in this order:

| Client ID | Client Name  | Client Email   |
|-----------|--------------|----------------|
| 1001      | Juan Pérez   | juan@example.com |
| 1002      | María López  | maria@example.com |

*You can adjust the script to accept more columns if needed.*

---

## 🎯 Usage Options

### Option 1: Console Script (Original)

1. Clone this repository or copy the code to your local project.
2. Open `script.py` and configure these variables:

# Carga de variables de entorno desde el archivo .env
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar las variables del archivo .env

sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
```

🔧 Configuración del archivo .env
Antes de ejecutar el script, crea un archivo .env en la raíz del proyecto y agrega tus credenciales de esta manera:
```python
SENDER_EMAIL=your_email@example.com
EMAIL_PASSWORD=your_password_or_app_password
```
3. Change the `smtp_server` and `smtp_port` if you're not using Outlook:

| Provider   | SMTP Server        | Port |
|------------|--------------------|------|
| Outlook    | smtp.office365.com | 587  |
| Gmail      | smtp.gmail.com     | 587  |

4. Run the script:
```bash
python script.py
```

### Option 2: Web Interface (NEW! 🌟)

1. **Set up the Django project**:
   ```bash
   cd automailsender
   python manage.py makemigrations emailapp
   python manage.py migrate
   ```

2. **Start the web server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the web interface**:
   Open your browser and go to: `http://127.0.0.1:8000/`

4. **Configure email settings**:
   - Click on "Settings" in the navigation
   - Enter your email credentials and SMTP settings
   - Save the configuration

5. **Send emails**:
   - **Single Email**: Use the "Send Email" page for individual emails
   - **Bulk Email**: Use the "Bulk Email" page to upload an Excel file and send to multiple recipients

---

## 🌐 Web Interface Guide

### Getting Started
1. **First Time Setup**: Navigate to Settings and configure your email credentials
2. **Email Settings**: Enter your email, password (or app password), SMTP server, and port
3. **Send Single Email**: Use the form to send an email to one recipient
4. **Send Bulk Emails**: Upload an Excel file and send personalized emails to multiple recipients
5. **View Logs**: Check the email history and delivery status

### Email Personalization
In bulk emails, you can use these placeholders that will be automatically replaced:
- `{client_name}` - Replaced with the client's name from the Excel file
- `{client_id}` - Replaced with the client's ID from the Excel file

Example:
```
Dear {client_name},

Your account ID {client_id} has been updated.

Best regards,
Your Company
```

### File Attachments
- Both single and bulk emails support file attachments
- You can attach multiple files at once
- All common file types are supported

---

## 📂 File Attachments

You can attach one or more files by:

**Console Script:**
```python
pdfFilePaths = [
    "C:\\path\\to\\your\\file1.pdf",
    "C:\\path\\to\\your\\file2.pdf"
]
```

**Web Interface:**
- Use the file upload field in the email forms
- Select multiple files by holding Ctrl (Windows) or Cmd (Mac)

---

## ▶️ Running the Application

### Console Version:
```bash
python script.py
```

### Web Interface:
```bash
cd automailsender
python manage.py runserver
```

---

## 🔧 Configuration

### Email Providers Setup

#### Gmail
1. Enable 2-factor authentication
2. Generate an App Password: Google Account → Security → App passwords
3. Use the app password instead of your regular password
4. SMTP settings: `smtp.gmail.com`, port `587`

#### Outlook/Office 365
1. If using 2FA, create an App Password: Microsoft Account → Security → Advanced Security Options
2. SMTP settings: `smtp.office365.com`, port `587`

#### Other Providers
Consult your email provider's documentation for SMTP settings.

---

## 📊 Features Comparison

| Feature | Console Script | Web Interface |
|---------|----------------|---------------|
| Send single emails | ❌ | ✅ |
| Send bulk emails | ✅ | ✅ |
| File attachments | ✅ | ✅ |
| Email personalization | ✅ | ✅ |
| User-friendly interface | ❌ | ✅ |
| Email logging | ❌ | ✅ |
| Settings management | ❌ | ✅ |
| Real-time feedback | ❌ | ✅ |
| Mobile responsive | ❌ | ✅ |
| Email history | ❌ | ✅ |

---

## 🚨 Troubleshooting

### Common Issues

**Authentication Error (535)**:
- Check your email and password
- For Gmail/Outlook with 2FA: Use an App Password
- Verify SMTP server settings

**File Upload Issues**:
- Ensure Excel files are in `.xlsx` or `.xls` format
- Check that the file has the required columns (ID, Name, Email)

**Email Not Sending**:
- Verify internet connection
- Check email provider's SMTP settings
- Ensure your account allows SMTP access

### Getting Help
1. Check the email logs in the web interface for detailed error messages
2. Verify your email settings in the Settings page
3. Test with a single email before attempting bulk sending

---

## 🔒 Security Notes

1. **Credentials**: Never commit your email credentials to version control
2. **App Passwords**: Use app-specific passwords when possible
3. **HTTPS**: Use HTTPS in production environments
4. **Environment Variables**: Store sensitive data in environment variables for production

---

## 🎉 Recent Updates

### Version 2.0 (Django Web Interface)
- Added complete Django web application
- User-friendly web interface with responsive design
- Email settings management through web forms
- Single and bulk email sending capabilities
- Email logging and history tracking
- File upload support for Excel files and attachments
- Real-time sending progress and results
- Bootstrap-based modern UI design

### Version 1.0 (Original Console Script)
- Console-based bulk email sending
- Excel file processing
- Basic email personalization
- File attachment support

---

## 📄 License

MIT License.

---

## ✍️ Authors

- **Mauricio Ibañez Bermudez** - Original console script
- **Abdulhameed Giwa** - Django web interface development

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change.