import numpy

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


def get_levenshtein_distance(s, t):
    rows = len(s) + 1
    cols = len(t) + 1
    distance = numpy.zeros((rows, cols), dtype=int)

    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0  # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                cost = 1
            distance[row][col] = min(
                distance[row - 1][col] + 1,  # Cost of deletions
                distance[row][col - 1] + 1,  # Cost of insertions
                distance[row - 1][col - 1] + cost,
            )
    return distance[row][col]


class PollResponseSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()
    attempts = serializers.SerializerMethodField()

    def validate(self, data):
        pr = PollResponse(response=data["response"], game=data["game"], poll=data["poll"])
        data["response"] = self.get_result(pr)["response"]
        return data

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

        normalized_resp = obj.response.lower()
        exact_match = [x["response"] for x in response_counts if x["response"] == normalized_resp]
        for index, data in enumerate(response_counts):
            current_resp = data["response"]
            if (
                normalized_resp in current_resp
                or (not exact_match and get_levenshtein_distance(normalized_resp, current_resp) < 3)
            ):
                return {
                    "points": data["count"],
                    "position": index,
                    "response": current_resp,
                }
        game = Game.objects.get(id=obj.game.id)
        game.attempts += 1
        game.save()
        if game.attempts > 2:
            raise serializers.ValidationError("GAME OVER")
        return {"points": 0, "position": -1, "response": normalized_resp}

    class Meta:
        model = PollResponse
        fields = ["response", "poll", "game", "result", "attempts"]
        validators = [
            UniqueTogetherValidator(
                queryset=PollResponse.objects.all(), fields=["response", "game"]
            )
        ]
