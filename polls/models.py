import uuid
from django.db import models


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    round = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)


class PollResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    response = models.TextField()
