from django.db import models

# Create your models here.

class MailTemplate( models.Model ):
    """
        Templates for Mails
        --fields--
        code: unique string-value to access the record.
        title: human readable name for the mail template
        subject: Subject for the mail
        plain_content: plain text content of the mail
        html_content: Alternative html based content for mail
        sender: email address to be user to send mail using this template, if empty mail is sent using settings.EMAIL_HOST_USER
        context: list of context variables that can be used in Content Body
    """
    code = models.CharField( max_length=5, unique=True, help_text="To be used by developers" )
    title = models.CharField( max_length=50, help_text="Human readable name of the template" )
    subject = models.CharField( max_length=200, help_text="Subject for the mail(max:200 Characters)" )
    plain_content = models.TextField( blank=True, null=True, help_text="Content of the mail")
    html_content = models.TextField( blank=True, null=True, help_text="HTML version of Content" )
    sender = models.EmailField(blank=True, null=True)
    context = models.TextField(blank=True, null=True, help_text="Values listed here can be used in Content body as django template variables. Values will be set from the current context. Example usage: {{name}}")

    def __unicode__( self ):
        return self.code