from rest_framework import serializers
from session.models import Session, Event, Param
from test.serializers import TestSerializer


class ParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Param
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField()
    params = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'uuid', 'started_at', 'finished_at', 'test', 'params', 'events', 'stdout', 'stderr']

    def get_test(self, session):
        serializer = TestSerializer(session.test, context=self.context)
        return serializer.data

    def get_params(self, session):
        params = session.params.order_by('key')
        serializer = ParamSerializer(params, many=True)
        return serializer.data

    def get_events(self, session):
        events = session.events.order_by('-time')
        serializer = EventSerializer(events, many=True)
        return serializer.data



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['time', 'status']
