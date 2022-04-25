import json
from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from session.models import Session, Param, Event
from session.serializers import SessionSerializer
from test.models import Test
from app import celery_app

from session.tasks import execute_session


def index(request):
    return HttpResponse("Session")


@csrf_exempt
def start_session(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        params = [Param(key=key, value=val) for key, val in body['params'].items()]
        test = Test.objects.get(id=body['test_id'])
        session = Session.objects.create(
            test=test,
        )
        session.params.set(params, bulk=False)
        session.uuid = str(execute_session.delay(session.id))
        session.save(update_fields=['uuid'])
        return HttpResponse("Success")


@csrf_exempt
def finish_session(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        try:
            session = Session.objects.get(id=body['id'])
            if session.finished_at is None:
                celery_app.control.revoke(session.uuid, terminate=True)
                session.finished_at = datetime.now()
                session.save(update_fields=['finished_at'])
                return HttpResponse("Success")
            else:
                return HttpResponse("The session is already finished")
        except Session.DoesNotExist:
            return HttpResponse("Does not exist")


@csrf_exempt
def update_session(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        event = body['event']
        session = Session.objects.get(id=body['id'])
        session.events.add(Event(status=event['status']), bulk=False)
        return HttpResponse("Success")


def get_sessions(request):
    if request.method == "GET":
        sessions = Session.objects.order_by('-started_at')
        response = json.dumps(SessionSerializer(sessions, many=True, context={'request': request}).data)
        return HttpResponse(response)
