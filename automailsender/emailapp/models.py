from django.db import models

class EmailSettings(models.Model):
    """Model to store email settings"""
    email = models.EmailField(verbose_name="Sender Email")
    password = models.CharField(max_length=255, verbose_name="Email Password")
    smtp_server = models.CharField(max_length=255, default="smtp.office365.com", verbose_name="SMTP Server")
    smtp_port = models.IntegerField(default=587, verbose_name="SMTP Port")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class EmailLog(models.Model):
    """Model to store email sending logs"""
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    
    recipient = models.EmailField(verbose_name="Recipient Email")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachment_names = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} - {self.subject} - {self.status}"

    class Meta:
        ordering = ['-sent_at']