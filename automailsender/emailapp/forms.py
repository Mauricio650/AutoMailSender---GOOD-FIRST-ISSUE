from django import forms
from .models import EmailSettings

class EmailSettingsForm(forms.ModelForm):
    """Form for email settings configuration"""
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = EmailSettings
        fields = ['email', 'password', 'smtp_server', 'smtp_port']

class SingleEmailForm(forms.Form):
    """Form for sending a single email"""
    recipient_email = forms.EmailField(label="Recipient Email")
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)
    attachments = forms.FileField(widget=forms.FileInput(attrs={'multiple': False}), required=False)

class BulkEmailForm(forms.Form):
    """Form for sending bulk emails"""
    excel_file = forms.FileField(label="Excel File (.xlsx)")
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea, help_text="You can use {client_name} and {client_id} as placeholders")
    attachments = forms.FileField(widget=forms.FileInput(attrs={'multiple': False}), required=False)