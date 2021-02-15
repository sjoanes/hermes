from rest_framework import generics
from django.shortcuts import render

from .models import Game
from .serializers import GameSerializer, PollResponseSerializer


class CreateGame(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = []


class CreatePollResponse(generics.CreateAPIView):
    serializer_class = PollResponseSerializer
    permission_classes = []


class PlayGame(generics.RetrieveAPIView):
    serializer_class = GameSerializer
    permission_classes = []
    queryset = Game.objects.all()

    def get_object(self):
        return self.get_queryset()[0]  # TODO: randomize
