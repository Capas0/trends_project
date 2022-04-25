from rest_framework import serializers
from .models import Test


class TestSerializer(serializers.ModelSerializer):
    script_url = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'name', 'script_url']

    def get_script_url(self, test):
        request = self.context.get('request')
        script_url = test.script.url
        return request.build_absolute_uri(script_url)
