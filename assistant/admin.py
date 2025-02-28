from django.contrib import admin

from .models import MessageHistory, Assistant


class MessageHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('message', 'timestamp')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'message' , 'timestamp')
        }),
    )

admin.site.register(MessageHistory, MessageHistoryAdmin)

admin.site.register(Assistant)