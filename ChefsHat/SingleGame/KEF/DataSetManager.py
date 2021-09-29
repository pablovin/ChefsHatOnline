# -*- coding: utf-8 -*-
import pandas as pd
from ..models import DataSet, Experiment, Rank, HumanObservation, AgentCompetitiveness, RivalryAgainstHuman, MemoryObservations, AgentCompetitiveness, HumanObservation, selfObservation, RivalryAgainstHuman

# Action types
actionDeal = "DEAL"
actionDiscard = "DISCARD"
actionNone = "NONE"
actionPizzaReady = "PIZZA_READY"
actionChangeRole ="ROLE_CHANGE"
actionSpecialAction = "SPECIAL_ACTION"
actionPass = "PASS"
actionFinish = "FINISH"
actionInvalid = "INVALID"


actionNewGame = "New_Game"


"""DataSet Manager Class

This class manages the function of the framework to create datasets. Here each datapoint is created, and written if necessary.


Attributes:
    dataSetDiretory (String): This variable keeps the directory which the dataSet files are stored.


Author: Pablo Barros
Created on: 26.02.2020
Last Update: 26.02.2020
"""

def saveRank(nickname, score):
    rank = Rank(nickName=nickname, score=score)
    rank.save()

def getRank():
    return Rank.objects.all().order_by("score")

def getAllExperiments():
    return Experiment.objects.all()

def getAllDBEntries(experiment):

    return DataSet.objects.filter(experiment=experiment).all().order_by("id")

def getMemoryObservations(experiment, player):
    return list(MemoryObservations.objects.filter(experiment=experiment).filter(player=player).all().order_by("id"))


def getHumanObservation(experiment, player):
    return list(HumanObservation.objects.filter(experiment=experiment).filter(player=player).all().order_by("id"))

def getSelfObservations(experiment, player):
    return list(selfObservation.objects.filter(experiment=experiment).filter(player=player).all().order_by("id"))

def getMyCompetitiviness(experiment, player):
    return list(AgentCompetitiveness.objects.filter(experiment=experiment).filter(player=player).all().order_by("id"))


def exportDBToFiles(savingPath):

    columns = ["Time", "Game Number", "Round Number", "Player", "Action Type", "Player Hand", "Board",
               "Possible Actions", "Cards Action", "Reward",
               "Qvalues", "Loss", "Wrong Actions", "Total Actions",  # Current turn actions
               "Scores", "Roles", "Players Status", "Agent Names", "Performance Score"  # Game status
               ]

    for experiment in getAllExperiments():
        savingFile = savingPath + experiment.name + ".pkl"
        savingCSV = savingPath+experiment.name + ".csv"
        allDbentries = getAllDBEntries(experiment)
        dataFrame = pd.DataFrame(columns=columns)
        for entry in allDbentries:
            dataPoint= [
                entry.time,
                entry.gameNumber ,
                entry.roundNumber ,
                entry.player,
                entry.actionType,
                entry.playerHand,
                entry.board,
                entry.possibleActions,
                entry.cardsAction,
                entry.reward ,
                entry.Qvalues,
                entry.loss,
                entry.wrongActions,
                entry.totalActions,
                entry.scores,
                entry.roles,
                entry.playerStatus,
                entry.agentNames,
                entry.performanceScore
            ]

            dataFrame.loc[-1] = dataPoint
            dataFrame.index = dataFrame.index + 1

        print ("Saving here:" + str(savingFile))
        dataFrame.to_pickle(savingFile)
        dataFrame.to_csv(savingCSV + ".csv", index=False, header=True)


def getexperimentModelDS(experimentName):
    return Experiment.objects.filter(name=experimentName).last()

def getLastEntryDS(experimentModel):

    return DataSet.objects.filter(experiment=experimentModel).last()

def startNewExperimentDS(experimentName):
    exp = Experiment(name=experimentName)
    exp.save()
    return exp

def startNewGameDS(expModel, gameNumber, agentsNames, roles, performanceScore):

    newPScore = []

    for a in performanceScore:
        newPScore.append(round(float(a),5))

    dataset = DataSet(
        experiment=expModel,
        gameNumber = gameNumber,
        roles = roles,
        agentNames = agentsNames,
        performanceScore = newPScore,
    )
    dataset.save()

def dealActionDS(expModel, playersHand, game, roles):

    actionType = actionDeal

    dataset = DataSet(
        experiment=expModel,
        actionType = actionType,
        playerHand = playersHand,
        gameNumber = game,
        roles = roles,
    )
    dataset.save()


def declareSpecialActionDS(expModel, player, playersHand, roles, cardsAction,  game):

    actionType = actionSpecialAction
    cardsAction = str(cardsAction)

    dataset = DataSet(
        experiment=expModel,
        actionType=actionType,
        player = player,
        playerHand = playersHand,
        cardsAction = [cardsAction],
        roles = roles,
        gameNumber = game
    )
    dataset.save()

def exchangeRolesActionDS(expModel, playersHand, roles, cardsAction,  game):

    newActionCards = []
    for a in cardsAction:

        newActionCards.append(str(a))

    # actionCards = cardsAction[1:-1].split(",")
    actionType = actionChangeRole

    # print("player hand:" + str(playersHand))
    # print("action cards:" + str(newActionCards))
    # input("here")

    dataset = DataSet(
        experiment=expModel,
        actionType=actionType,
        playerHand = playersHand,
        cardsAction = newActionCards,
        roles = roles,
        gameNumber = game
    )
    dataset.save()

def doActionActionDS(expModel, game, player, roundNumber, action, board, wrongActions, reward,
                   playersHand, roles, score, playersStatus, qValue, loss, totalActions, possibleActions):

    actionType = action.split("_")[0]
    actionCards = action.split("_")[1][1:-1].split(",")
    # if actionCards[0] == "":
    #     actionCards = []

    # actionCards = str(actionCards)

    qValue = qValue.tolist()
    # print ("actionCards:" + str(actionCards))
    # input("here")

    # guarantee is a list
    # score = score.tolist()
    # playersHand = playersHand.tolist()
    # board = board.tolist()
    # reward = reward.tolist()
    # print("Qvalues:" + str(qValue))

    # print ("Qvalues:" +str(qValue))
    # print("Qvalues:" + str(len(qValue)))
    # loss = loss.tolist()
    # roles = roles.tolist()
    # playersStatus = playersStatus.tolist()
    # print ("player hand:" + str(playersHand))
    # print ("board:" + str(board))
    # print("roles:" + str(roles))
    # print ("score:"+ str(score))
    # print ("qvalues:" + str(qValue))
    # print ("loss:" + str(loss))
    # print ("Player status:" + str(playersStatus))
    # print ("possible actions:" + str(possibleActions))
    # print("action cards:" + str(actionCards))
    dataset = DataSet(
        experiment = expModel,
        gameNumber=game,
        roundNumber=roundNumber,
        player=player,
        actionType=actionType,
        playerHand=playersHand,
        board=board,
        cardsAction=actionCards,
        reward=reward,
        Qvalues=qValue,
        loss=loss,
        wrongActions=wrongActions,
        totalActions=totalActions,
        scores=score,
        roles=roles,
        playerStatus=playersStatus,
        possibleActions=possibleActions
    )
    dataset.save()


def doActionPizzaReadyDS(expModel, roundNumber, board, playersHand, roles, score, playersStatus, game):

    actionType = actionPizzaReady

    # print ("board:" + str(board))
    # print ("playersHand:"+str(playersHand))
    # print ("roles:" + str(roles))
    # print ("scores:" + str(score))
    # print ("playersStatus:"+str(playersStatus))
    dataset = DataSet(
        experiment = expModel,
        actionType=actionType,
        playerHand=playersHand,
        scores=score,
        roundNumber=roundNumber,
        board=board,
        roles=roles,
        playerStatus=playersStatus,
        gameNumber=game)

    dataset.save()

def saveObservation(expModel, player, state, action, reward, next_state, done, possibleActions, newPossibleActions):
    # pass

    state = state.tolist()
    next_state = next_state.tolist()
    # print ("State:" + str(state))
    # print ("Next state:" + str(next_state))
    # print ("Action:" + str(action))
    # print ("Done:" + str(done))
    dataset = MemoryObservations(
    experiment = expModel,
    player  =  player,
    state = state,
    action =  action,
    reward = reward,
    next_state = next_state,
    done = done,
    possibleActions = possibleActions,
    new_possibleActions = newPossibleActions
    )

    dataset.save()


def addCompetitiveness(expModel, player, competitiveness, match, round):
    dataset = AgentCompetitiveness(
    experiment = expModel,
    player  =  player,
    myCompetitiveness = competitiveness,
    match =  match,
    round = round
    )

    dataset.save()

def observeHuman(expModel, player, observationHuman, match, round):
    # pass


    dataset = HumanObservation(
    experiment = expModel,
    player  =  player,
    observationHuman = observationHuman,
    match =  match,
    round = round
    )

    dataset.save()

def selfObserve(expModel, player, observation, match, round):
    # pass


    dataset = selfObservation(
        experiment=expModel,
        player=player,
        observation=observation,
        match=match,
        round=round
    )

    dataset.save()

def saveRivalry(expModel, player, rivalry, match, rounds):
    # pass

    rivalry = round(rivalry, 4)

    dataset = RivalryAgainstHuman(
        experiment=expModel,
        player=player,
        rivalry=rivalry,
        match=match,
        round=rounds
    )

    dataset.save()