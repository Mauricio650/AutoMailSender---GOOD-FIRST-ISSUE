from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

from .forms import EmailSettingsForm, SingleEmailForm, BulkEmailForm
from .models import EmailSettings, EmailLog
from .email_utils import send_single_email, send_bulk_emails


def home(request):
    """Home page view"""
    return render(request, 'emailapp/home.html')


@csrf_protect
def email_settings(request):
    """Email settings configuration view"""
    # Check if settings already exist
    settings_instance = EmailSettings.objects.first()
    
    if request.method == 'POST':
        form = EmailSettingsForm(request.POST, instance=settings_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Email settings saved successfully.")
            return redirect('home')
    else:
        form = EmailSettingsForm(instance=settings_instance)
    
    return render(request, 'emailapp/settings.html', {'form': form})


@csrf_protect
def send_email(request):
    """Single email sending view"""
    # Check if email settings exist
    email_settings = EmailSettings.objects.first()
    if not email_settings:
        messages.error(request, "Please configure email settings first.")
        return redirect('email_settings')
    
    if request.method == 'POST':
        form = SingleEmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            
            # Handle file attachments
            attachments = request.FILES.getlist('attachments')
            
            # Send the email
            success, message = send_single_email(
                email_settings.email,
                email_settings.password,
                recipient_email,
                subject,
                body,
                attachments
            )
            
            # Log the email
            attachment_names = ", ".join([attachment.name for attachment in attachments]) if attachments else None
            EmailLog.objects.create(
                recipient=recipient_email,
                subject=subject,
                body=body,
                attachment_names=attachment_names,
                status='success' if success else 'failed',
                error_message=None if success else message
            )
            
            if success:
                messages.success(request, "Email sent successfully.")
            else:
                messages.error(request, f"Failed to send email: {message}")
            
            return redirect('send_email')
    else:
        form = SingleEmailForm()
    
    # Get recent email logs
    recent_logs = EmailLog.objects.all()[:10]
    
    return render(request, 'emailapp/send_email.html', {
        'form': form,
        'recent_logs': recent_logs
    })


@csrf_protect
def bulk_email(request):
    """Bulk email sending view"""
    # Check if email settings exist
    email_settings = EmailSettings.objects.first()
    if not email_settings:
        messages.error(request, "Please configure email settings first.")
        return redirect('email_settings')
    
    if request.method == 'POST':
        form = BulkEmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Get form data
            excel_file = request.FILES['excel_file']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            
            # Handle file attachments
            attachments = request.FILES.getlist('attachments')
            
            # Send bulk emails
            success, results = send_bulk_emails(
                email_settings.email,
                email_settings.password,
                excel_file,
                subject,
                body,
                attachments
            )
            
            if success:
                # Log each email
                attachment_names = ", ".join([attachment.name for attachment in attachments]) if attachments else None
                
                success_count = 0
                fail_count = 0
                
                for result in results:
                    if result['status'] == 'Success':
                        success_count += 1
                    else:
                        fail_count += 1
                
                messages.success(request, f"Bulk email process completed. {success_count} emails sent successfully, {fail_count} failed.")
                
                # Return results to template
                return render(request, 'emailapp/bulk_results.html', {
                    'results': results
                })
            else:
                messages.error(request, f"Error processing bulk emails: {results}")
    else:
        form = BulkEmailForm()
    
    return render(request, 'emailapp/bulk_email.html', {
        'form': form
    })


def email_logs(request):
    """View all email logs"""
    logs = EmailLog.objects.all()
    return render(request, 'emailapp/logs.html', {'logs': logs})