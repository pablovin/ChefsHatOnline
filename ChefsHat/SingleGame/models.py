from django.db import models
from django.contrib.postgres.fields import ArrayField

class Rank(models.Model):
    time = models.DateTimeField(auto_now=True)
    nickName = models.CharField(default="", max_length=500)
    score = models.FloatField(blank=True)

class Experiment(models.Model):

    name = models.CharField(max_length=300)

class DataSet(models.Model):

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    gameNumber =  models.CharField(default="", max_length=4)
    roundNumber = models.CharField(default="", max_length=4)
    player =  models.CharField(default="", max_length=2)
    actionType = models.CharField(max_length=50)
    playerHand = ArrayField(ArrayField(models.IntegerField(blank=True, default=list)), default=list)
    board = ArrayField(models.IntegerField(blank=True), default=list)
    possibleActions = ArrayField(models.IntegerField(blank=True),  default=list)
    cardsAction = ArrayField(models.CharField(max_length=500), default=list)
    reward = models.CharField(max_length=10, default ="")
    Qvalues = ArrayField(models.CharField(max_length=8),  default=list)
    loss = models.CharField(max_length=20, default ="")
    wrongActions = models.CharField(max_length=10, default ="")
    totalActions = models.CharField(max_length=10, default ="")
    scores = ArrayField(models.IntegerField(blank=True),  default=list)
    roles = ArrayField(models.IntegerField(blank=True),  default=list)
    playerStatus = ArrayField(ArrayField(models.CharField(max_length=500,default="")), default=list)
    agentNames = ArrayField(models.CharField(blank=True, max_length=50),  default=list)
    performanceScore = ArrayField(models.FloatField(blank=True),  default=list)

# Create your models here.

class MemoryObservations(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    player  =  models.CharField(default="", max_length=300)
    state = ArrayField(models.FloatField(blank=True), default=list)
    action =  models.CharField(default="", max_length=4)
    reward = models.CharField(max_length=300, default ="")
    next_state = ArrayField(models.FloatField(blank=True), default=list)
    done = models.CharField(max_length=300, default ="")
    possibleActions = ArrayField(models.IntegerField(blank=True), default=list)
    new_possibleActions = ArrayField(models.IntegerField(blank=True), default=list)


class AgentCompetitiveness(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    player = models.CharField(default="", max_length=300)
    myCompetitiveness = models.FloatField(blank=True)
    match = models.CharField(default="", max_length=10)
    round = models.CharField(default="", max_length=10)


class HumanObservation(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    player = models.CharField(default="", max_length=300)
    observationHuman = ArrayField(models.FloatField(blank=True), default=list)
    match = models.CharField(default="", max_length=10)
    round = models.CharField(default="", max_length=10)

class selfObservation(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    player = models.CharField(default="", max_length=300)
    observation = ArrayField(models.FloatField(blank=True), default=list)
    match = models.CharField(default="", max_length=10)
    round = models.CharField(default="", max_length=10)

class RivalryAgainstHuman(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    player = models.CharField(default="", max_length=300)
    rivalry = models.CharField(max_length=300, default ="")
    match = models.CharField(default="", max_length=10)
    round = models.CharField(default="", max_length=10)
