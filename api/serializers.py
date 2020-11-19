from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_username')

    @staticmethod
    def get_username(obj):
        return obj.author.username

    class Meta:
        model = Message
        fields = ['author', 'text']
