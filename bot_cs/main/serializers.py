from main.models import Bots
from rest_framework import serializers


class BotsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bots
        fields = ['comment', 'login', 'password', 'steamid','shared_secret','steamAPI','googleDriveId','proxy']

class BotsShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bots
        fields = ['comment', 'login']

