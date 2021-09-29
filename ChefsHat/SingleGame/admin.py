from django.contrib import admin
from .models import DataSet, Experiment, Rank, MemoryObservations, HumanObservation, AgentCompetitiveness, RivalryAgainstHuman
#
admin.site.register(Experiment)
admin.site.register(DataSet)
admin.site.register(Rank)
admin.site.register(MemoryObservations)
admin.site.register(AgentCompetitiveness)
admin.site.register(HumanObservation)
admin.site.register(RivalryAgainstHuman)

# Register your models here.
