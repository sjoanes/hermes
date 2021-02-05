from rest_framework import serializers

from .models import Game, Poll, PollResponse

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ["id", "description"]

class GameSerializer(serializers.ModelSerializer):
    current_poll = PollSerializer(read_only=True) 

    def create(self, validated_data):
        poll = Poll.objects.create(
            description="What sports are taught in school?",
        )
        return Game.objects.create(
            current_poll=poll,
        )

    class Meta:
        model = Game
        fields = [
            "id",
            "current_poll",
            "round",
            "points",
            "attempts",
        ]

class PollResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollResponse
        fields = ["response", "poll", "game"]

