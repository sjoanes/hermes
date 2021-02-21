from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Count

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


class PollResponseSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    attempts = serializers.SerializerMethodField()

    def validate_response(self, value):
        return value.lower()

    def get_attempts(self, obj):
        return obj.game.attempts

    def get_result(self, obj):
        response_counts = (
            PollResponse.objects.filter(poll=obj.poll.id)
            .values("response")
            .annotate(count=Count("response"))
            .filter(count__gt=1)
            .order_by("-count")
        )[:8]
        for index, data in enumerate(response_counts):
            if obj.response.lower() in data["response"]:
                return {
                    "points": data["count"],
                    "position": index,
                }
        game = Game.objects.get(id=obj.game.id)
        game.attempts += 1
        game.save()
        if game.attempts > 2:
             raise serializers.ValidationError("GAME OVER")
        return { "points": 0, "position": -1 }


    class Meta:
        model = PollResponse
        fields = ["response", "poll", "game", "result", "attempts"]
        validators = [
            UniqueTogetherValidator(
                queryset=PollResponse.objects.all(), fields=["response", "game"]
            )
        ]
