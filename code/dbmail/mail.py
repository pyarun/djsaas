'''
Created on 07-May-2012

@author: arun
'''
from django.core.mail import EmailMultiAlternatives, mail_admins, mail_managers
from django.template.loader import get_template
from django.template import Context, Template
from django.conf import settings

from models import MailTemplate


class DbSendMail:
    """
        Manager for sending preset mails
    """

    def __init__( self, mail_code ):
            self.mail = MailTemplate.objects.get( code=mail_code )

    def sendmail(self, recipient_list, context, bcc=None, cc=None):
        """
            @recipient_list: recievers email addresses
            context: dict. values to be updated in template
        """
        self._feed_mail_contents( context )
        subject = self.mail.subject
        from_email = self.mail.sender or settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives( subject, self.plain_content, from_email, recipient_list ,bcc=bcc, cc=cc)
        if self.html_content: msg.attach_alternative( self.html_content, "text/html" )
        msg.send()

    def _feed_mail_contents( self, context ):
        plain_content = Template( self.mail.plain_content )
        self.plain_content = plain_content.render( Context( context ) )
        if self.mail.html_content:
            html_content = Template( self.mail.html_content )
            self.html_content = html_content.render( Context( context ) )
        else:
            self.html_content = None

    def mail_admins( self, context ):
        self._feed_mail_contents( context )
        subject = self.mail.subject
#        from_email = self.mail.sender
        msg = self.plain_content
        mail_admins( subject, msg )

    def mail_managers( self, context ):
        self._feed_mail_contents( context )
        subject = self.mail.subject
#        from_email = self.mail.sender
        msg = self.plain_content
        mail_managers( subject, msg )
