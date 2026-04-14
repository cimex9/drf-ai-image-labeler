from rest_framework import serializers

from app.models import Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'description', 'created_at']


class AskWithImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    question = serializers.CharField(max_length=500)
