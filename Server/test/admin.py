from django.contrib import admin
from .models import Test
from session.models import Session
from session.tasks import execute_session


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    actions = ['run_test']

    @admin.action(description='Run selected tests')
    def run_test(self, request, queryset):
        for test in queryset:
            session = Session.objects.create(
                test=test,
            )
            session.uuid = str(execute_session.delay(session.id))
            session.save(update_fields=['uuid'])
