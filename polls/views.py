from rest_framework import generics
from django.shortcuts import render

from .models import Game
from .serializers import GameSerializer, PollResponseSerializer


class CreateGame(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = []

    def get_serializer_context(self):
        return self.request.data

class CreatePollResponse(generics.CreateAPIView):
    serializer_class = PollResponseSerializer
    permission_classes = []
