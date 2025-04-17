
# 📧 AutoMailSender

This project is an automation tool for sending bulk emails to a list of clients defined in an Excel file. It is ideal for administrative tasks, reminders, notifications, or any email flow that needs to be personalized.

---

## 🚀 Features

- ✅ Load client data from an Excel file (`.xlsx`)
- ✅ Automatically generate a personalized message for each client
- ✅ Attach files to the email
- ✅ Use SMTP (compatible with Outlook, Gmail, etc.)
- ✅ Validate emails before sending
- ✅ Modular structure, easy to maintain

---

## 🛠️ Requirements

- Python 3.10 or higher
- Python packages: `pandas` `openpyxl`

Install them by running:

```
pip install pandas openpyxl
```

---

## 🧩 Project Structure

```
📂 AutoMailSender/
├── script.py           # Main script
├── Libro.xlsx          # File with client data (col: ID, Name, Email)
```

---

## 📋 Excel File Format (`Libro.xlsx`)

It should have at least three columns in this order:

| Client ID | Client Name  | Client Email   |
|-----------|--------------|----------------|
| 1001      | Juan Pérez   | juan@example.com |
| 1002      | María López  | maria@example.com |

*You can adjust the script to accept more columns if needed.*

---

## ✉️ How to Set Up

1. Clone this repository or copy the code to your local project.
2. Open `script.py` and configure these variables:

```python
sender_email = "your_email@example.com"
password = "YOUR_PASSWORD_OR_APP_PASSWORD"
```

3. Change the `smtp_server` and `smtp_port` if you're not using Outlook:

| Provider   | SMTP Server        | Port |
|------------|--------------------|------|
| Outlook    | smtp.office365.com | 587  |
| Gmail      | smtp.gmail.com     | 587  |

> ⚠️ If you are using Gmail, you will need to generate an **app password** and enable **two-factor authentication**.

4. Ensure the Excel file and attachment files exist in the indicated paths or edit the paths in the code.

---

## 📂 Attachments

You can attach one or more files by modifying this part:

```python
pdfFilePaths = [
    "C:\Users\INTEL\Downloads\SRS_Plantilla_Con_Portada_Bordes_Contenido.pdf"
]
```

---

## ▶️ How to Run

From the terminal:

```bash
python script.py
```

Or, if you are using a virtual environment:

```bash
venv\Scripts\python.exe script.py
```

---

## 📌 Additional Notes

- You can adjust the email sending range in this line:

```python
for initialCounter in range(0, 2):
```

- You can also include additional validations before sending emails.
- The script can update the Excel file in case of invalid data (like missing emails).

---

## 📄 License

MIT License.

---

## ✍️ Author

Mauricio Ibañez Bermudez
