
from django.contrib import admin
from models import MailTemplate



class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "sender")
#    fields = ('code', 'title', 'sender', 'subject', 'context', 'plain_content', 'html_content')
#    field_options = {
#        "fields": (('code', 'title'), 'sender', 'subject', 'context', 'plain_content', 'html_content')
#    }
#    
    
    fieldsets = ((None,  {"fields": (('code', 'title'),)} 
                 ),
                 ("Details", {"fields": ('sender', 'subject', 'context', 'plain_content', 'html_content')}),
            )

admin.site.register(MailTemplate, MailTemplateAdmin)