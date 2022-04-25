from datetime import datetime

from django.utils.html import format_html
from django.contrib import admin
from .models import Session
from app import celery_app


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'uuid', 'started_at', 'finished_at', 'stdout', 'stderr')
    actions = ['stop_session']

    def stdout(self, session):
        filepath = f'/files/data/{session.test.name}/{session.uuid}/stdout.txt'
        return format_html("<a href='{url}'>stdout</a>", url=filepath)

    def stderr(self, session):
        filepath = f'/files/data/{session.test.name}/{session.uuid}/stderr.txt'
        return format_html("<a href='{url}'>stderr</a>", url=filepath)

    @admin.action(description='Stop selected sessions')
    def stop_session(self, request, queryset):
        for session in queryset:
            if session.finished_at is not None:
                continue
            celery_app.control.revoke(session.uuid, terminate=True)
            session.finished_at = datetime.now()
            session.save(update_fields=['finished_at'])
