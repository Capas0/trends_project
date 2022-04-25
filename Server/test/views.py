import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Test
from .serializers import TestSerializer


def index(request):
    return HttpResponse("Test")


@csrf_exempt
def add_test(request):
    if request.method == "POST":
        body = json.loads(request.POST['body'])
        if (script := request.FILES.get('script')) is None:
            return HttpResponseBadRequest("The script file is not specified")

        Test.objects.create(
            name=body.get('name'),
            script=script,
        )
        return HttpResponse("Success")


@csrf_exempt
def delete_test(request):
    if request.method == "DELETE":
        try:
            test = Test.objects.get(id=request.GET['id'])
            test.delete()
            return HttpResponse("Success")
        except Test.DoesNotExist:
            return HttpResponse("Does not exist")


def get_tests(request):
    if request.method == "GET":
        tests = Test.objects.all()
        response = json.dumps(TestSerializer(tests, many=True, context={'request': request}).data)
        return HttpResponse(response)
