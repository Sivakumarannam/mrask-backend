from rest_framework import serializers

from .models import ContactMessage, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'slug', 'title', 'tagline', 'role', 'summary', 'highlights', 'stack',
            'steps', 'github_url', 'demo_url', 'demo_kind',
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

    def validate_message(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('Message is too short.')
        return value.strip()
