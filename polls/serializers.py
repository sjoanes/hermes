from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Game, Poll, PollResponse


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ["id", "description"]


class GameSerializer(serializers.ModelSerializer):
    current_poll = PollSerializer(read_only=True)

    def create(self, validated_data):
        poll = Poll.objects.all()[
            0
        ]  # .create(description="What sports are taught in school?",)
        return Game.objects.create(current_poll=poll,)

    class Meta:
        model = Game
        fields = [
            "id",
            "current_poll",
            "round",
            "points",
            "attempts",
        ]


class LitGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["attempts"]


class PollResponseSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    attempts = serializers.SerializerMethodField()

    def get_attempts(self, obj):
        return obj.game.attempts

    def get_points(self, obj):
        points = (
            len(PollResponse.objects.filter(response=obj.response, poll=obj.poll.id))
            - 1
        )
        if points == 0:
            game = Game.objects.get(id=obj.game.id)
            game.attempts += 1
            game.save()
            if game.attempts > 2:
                raise serializers.ValidationError("GAME OVER")
        return points

    class Meta:
        model = PollResponse
        fields = ["response", "poll", "game", "points", "attempts"]
        validators = [
            UniqueTogetherValidator(
                queryset=PollResponse.objects.all(), fields=["response", "game"]
            )
        ]
