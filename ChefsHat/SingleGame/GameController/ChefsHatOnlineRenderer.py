import numpy
import random
import datetime
# from SingleGame.models import User, Game, Actions
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.staticfiles.storage import staticfiles_storage

from SingleGame.KEF.DataSetManager import actionFinish, actionDiscard, actionPass, actionDeal, actionInvalid, actionNewGame, actionChangeRole, actionPizzaReady, actionSpecialAction

from SingleGame.KEF.DataSetManager import getLastEntryDS

import cv2

import pandas as pd

import os

# from SingleGame.KEF.DataSetManager import DataSetManager

def getPlayingField():
    return cv2.imread(settings.BASE_DIR + settings.STATIC_URL + "images/playingField.png")

def getHandCardsDirectory(playerHand):
    cardsDirectory = []

    for a in playerHand:
        if not a == 0:
            cardsDirectory.append( "/deck" + "/" + str(a)+".png")

    # import sys
    # print("---------", file=sys.stderr)
    # print("Cards:" + str(len(cardsDirectory)), file=sys.stderr)
    return cardsDirectory

def getCards():
    cards = {}
    cardImages = os.listdir(settings.BASE_DIR + settings.STATIC_URL + "images/deck")
    cardImages.sort(key=lambda f: int(f.split(".")[0]))
    cardNumber = 1
    for card in cardImages:
        # self.cards[cardNumber] = cv2.resize(numpy.array(cv2.imread(self.resourcesFolder+"/"+self.cardsDirectory+"/"+card)), (141,195))
        cards[cardNumber] = cv2.resize(
            numpy.array(cv2.imread(settings.BASE_DIR + settings.STATIC_URL + "images/deck/" + card)), (140, 180))
        cardNumber = cardNumber + 1

    # Pass Card
    passCard = numpy.array(cv2.resize(cv2.imread(settings.BASE_DIR + settings.STATIC_URL+"images/actionCards/pass.png"), (176, 243)))

    #Rolecards
    roleCards = []

    roleCards.append(cv2.resize(cv2.imread(settings.BASE_DIR + settings.STATIC_URL+"images/actionCards/chef.png"), (176, 243)))

    roleCards.append(
        cv2.resize(cv2.imread(settings.BASE_DIR + settings.STATIC_URL+"images/actionCards/souschef.png"),
                   (176, 243)))
    roleCards.append(
        cv2.resize(cv2.imread(settings.BASE_DIR + settings.STATIC_URL+"images/actionCards/wait.png"), (176, 243)))

    roleCards.append(
        cv2.resize(cv2.imread(settings.BASE_DIR + settings.STATIC_URL+"images/actionCards/dishwasher.png"),
                   (176, 243)))

    #Back card
    backCard = numpy.array(
        cv2.resize(cv2.imread(settings.BASE_DIR + settings.STATIC_URL + "images/cardBack.png"), (140, 180)))

    #Black card
    blackCard = numpy.zeros((180,140,3))


    #Special move cards
    specialCards = []

    specialCards.append( cv2.resize(
            numpy.array(cv2.imread(settings.BASE_DIR + settings.STATIC_URL + "images/actionCards/cardDinner.png")), (140, 180)))

    specialCards.append( cv2.resize(
            numpy.array(cv2.imread(settings.BASE_DIR + settings.STATIC_URL + "images/actionCards/cardFight.png")), (140, 180)))

    return cards,passCard,roleCards,blackCard, backCard, specialCards


def drawBoard(originalImage, board, cards):
    currentBoardPlace = 0

    for i in range(len(board)):
        if int(board[i]) > 0 and not int(board[i]) == 13:
            card = numpy.array(cards[int(board[i])])
            card = numpy.array(cv2.resize(card, (240, 332)))

            if currentBoardPlace < 3:
                yPosition = 1095
                xPosition = 575 + (currentBoardPlace * 300)
            elif currentBoardPlace >= 3 and currentBoardPlace < 8:
                yPosition = 1495
                xPosition = 272 + ((currentBoardPlace - 3) * 300)
            elif currentBoardPlace >= 8:
                yPosition = 1895
                xPosition = 575 + ((currentBoardPlace - 8) * 225)

            originalImage[
                yPosition:yPosition + card.shape[0],
                xPosition:xPosition + card.shape[1]
            ] = card

        currentBoardPlace = currentBoardPlace + 1

    return originalImage


def getBoard(board, cards, roleCards, passCard, actionType, playerStatus, roles):

    playingField = getPlayingField()
    playingField = numpy.array(playingField)
    playingField = drawRoleCard(playingField, roles, roleCards)

    if not (actionType == actionDeal or actionType==actionChangeRole or actionType == actionSpecialAction):
        playingField = drawBoard(playingField, board, cards)
        playingField = drawPassCard(playingField, playerStatus, passCard)

    playingField = cv2.resize(playingField, (600, 800))

    return playingField


def drawPassCard(originalImage, playerCurrentStatus, card):
    card = numpy.array(cv2.resize(card, (240, 332)))

    # 1
    if (len(playerCurrentStatus[0]) > 0 and actionPass in playerCurrentStatus[0]):
        yPosition = 1025
        xPosition = 160

        originalImage[
            yPosition:yPosition + card.shape[0],
            xPosition:xPosition + card.shape[1]
        ] = card

    # 2
    if (len(playerCurrentStatus[1]) > 0 and actionPass in playerCurrentStatus[1]):
        yPosition = 1952
        xPosition = 157

        originalImage[
            yPosition:yPosition + card.shape[0],
            xPosition:xPosition + card.shape[1]
        ] = card

    # 3
    if (len(playerCurrentStatus[2]) > 0 and actionPass in playerCurrentStatus[2]):
        yPosition = 1955
        xPosition = 1588

        originalImage[
            yPosition:yPosition + card.shape[0],
            xPosition:xPosition + card.shape[1]
        ] = card

    # 4
    if (len(playerCurrentStatus[3]) > 0 and actionPass in playerCurrentStatus[3]):
        yPosition = 1025
        xPosition = 1615

        originalImage[
            yPosition:yPosition + card.shape[0],
            xPosition:xPosition + card.shape[1]
        ] = card

    return originalImage


def drawRoleCard(originalImage, roles, roleCards):

    if len(roles) > 0:
        positions = [
            [515, 28],
            [2455, 29],
            [2453, 1713],
            [512, 1720]
        ]

        for pIndex, position in zip(range(4), positions):
            card = roleCards[roles[pIndex]]
            card = numpy.array(cv2.resize(card, (236, 323)))
            yPosition = position[0]
            xPosition = position[1]

            originalImage[
                yPosition:yPosition + card.shape[0],
                xPosition:xPosition + card.shape[1]
            ] = card

    return originalImage


def getPlayerCards(playerHand, cards, blackCard, backCard, actionType, displayPlayer):

    if not actionType == "":

        # display player card
        if displayPlayer:
            # image = numpy.zeros((1000, 620, 3))
            image = numpy.zeros((400, 1400, 3))
            row = 0
            yPosition = 0
            xPosition = 10
            for i in range(len(playerHand)):
                if playerHand[i] == 0:
                    card = blackCard
                else:
                    card = cards[playerHand[i]]

                if i % 9 == 0:
                    # yPosition = yPosition + card.shape[0] + 10
                    yPosition = row*card.shape[0] + row*10 + 10
                    xPosition = 10
                    row = row + 1
                else:
                    xPosition = xPosition + card.shape[1] + 10
                image[yPosition:yPosition + card.shape[0], xPosition:xPosition + card.shape[1]] = card
            # image = cv2.resize(image, (300, 500))
            image = cv2.resize(image, (400, 125))

        else:
            image = numpy.zeros((400, 1400, 3))
            row = 0
            yPosition = 0
            xPosition = 0
            for i in range(len(playerHand)):
                if playerHand[i] == 0:
                    card = blackCard
                else:
                    card = backCard
                if i % 9 == 0:
                    # yPosition = yPosition + card.shape[0] + 10
                    yPosition = row * card.shape[0] + 10 + row*10
                    xPosition = 0
                    row = row + 1
                else:
                    xPosition = xPosition + card.shape[1] + 10
                image[yPosition:yPosition + card.shape[0], xPosition:xPosition + card.shape[1]] = card
            image = cv2.resize(image, (400, 125))


        return image

def drawPossibleActions(possibleActions, cards, passCard):

    images = []
    testIndex = 0
    for p in possibleActions:
        if p == "pass":
            resizedPass = cv2.resize(passCard,(140, 180))
            actionImage = numpy.zeros((cards[1].shape[0], cards[1].shape[1] * 8, 3))
            actionImage[0:resizedPass.shape[0], 0: resizedPass.shape[1]] = resizedPass
            images.append(cv2.resize(actionImage, (200, 30)))
        else:
            action= p.split(";")
            cardValue = int(action[0][1:])-1
            quantity = int(action[1][1:])
            jokerQuantity = int(action[2][1:])

            # import sys
            # print("---------", file=sys.stderr)
            # print("CardValue:" + str(cardValue), file=sys.stderr)
            # print("Quantity:" + str(quantity), file=sys.stderr)
            # print("Joker:" + str(jokerQuantity), file=sys.stderr)
            # print("Cards:" + str(cards[1].shape), file=sys.stderr)

            #add the cards
            cardsAction = []
            for q in range(quantity):
                cardValueIndex = cardValue+1
                cardsAction.append(cards[cardValueIndex])

            #add Joker
            for q in range(jokerQuantity):
                cardsAction.append(cards[12])

            # actionImage = numpy.zeros((cards[1].shape[0]*len(cardsAction)+10*len(cardsAction), cards[1].shape[1], 3))
            actionImage = numpy.zeros((cards[1].shape[0], cards[1].shape[1] * 8, 3))


            # print("Cards Action:" + str(len(cardsAction)), file=sys.stderr)

            initialX = 0
            for indexC, c in enumerate(cardsAction):
                # print(" --- C:" + str(len(c)), file=sys.stderr)
                actionImage[0:c.shape[0], initialX:initialX+c.shape[1]] = c
                initialX = ((indexC+1)*c.shape[1])

                testIndex = testIndex+1

            actionImage = cv2.resize(actionImage,(200,30))
            images.append(actionImage)

    return images


def renderCurrentDataset(expModel, drawBoard=True, withSpecialCards=False):

    # # dataSetDirectory = staticfiles_storage.path(expName)
    # # dataSetDirectory = settings.BASE_DIR+settings.STATIC_URL+expName
    # # readFile = pd.read_pickle(dataSetDirectory+"/Dataset.pkl")
    # #
    print ("expModel:" + str(expModel))
    dataSetDirectory = settings.BASE_DIR+settings.STATIC_URL+expModel.name
    #
    # dsManager = DataSetManager(dataSetDirectory=dataSetDirectory)
    # dsManager._currentDataSetFile = dataSetDirectory + "/Dataset.pkl"
    # dsManager.loadDataFrame(dataFrame)

    currentAction = getLastEntryDS(expModel)

    actionType = currentAction.actionType

    playerHand = currentAction.playerHand
    board = currentAction.board
    playerStatus = currentAction.playerStatus
    roles = currentAction.roles

    # import sys
    # print("actionType:" + str(actionType), file=sys.stderr)
    # print("playerHand:" + str(playerHand), file=sys.stderr)
    # print("board:" + str(board), file=sys.stderr)
    # print("playerStatus:" + str(playerStatus), file=sys.stderr)

    #Load the cards image
    cards,passCard,roleCards,blackCard, backCard, specialCards = getCards()

    # #Draw Players cards
    # p1Cards = getPlayerCards(playerHand[0], cards, blackCard, backCard, actionType, True)
    # p2Cards = getPlayerCards(playerHand[1], cards, blackCard, backCard, actionType, False)
    # p3Cards = getPlayerCards(playerHand[2], cards, blackCard, backCard, actionType, False)
    # p4Cards = getPlayerCards(playerHand[3], cards, blackCard, backCard, actionType, False)

    # Draw the board
    if drawBoard:
        boardImage = getBoard(board, cards, roleCards, passCard, actionType, playerStatus, roles)
        cv2.imwrite(dataSetDirectory + "/" + "currentBoard.png", boardImage)

    # #Draw the highlevel Actions
    # if len(highLevelActions) > 0:
    #     imagesPossibleActions = drawPossibleActions(highLevelActions, cards, passCard)
    #     for aIndex, a in enumerate(imagesPossibleActions):
    #         cv2.imwrite(dataSetDirectory + "/" + str(highLevelActions[aIndex])+".png", a)
    #
    # cv2.imwrite(dataSetDirectory+"/"+"p1Cards.png",p1Cards)
    # cv2.imwrite(dataSetDirectory+"/"+"p2Cards.png",p2Cards)
    # cv2.imwrite(dataSetDirectory+"/"+"p3Cards.png",p3Cards)
    # cv2.imwrite(dataSetDirectory+"/"+"p4Cards.png",p4Cards)



    player1Cards = getHandCardsDirectory(playerHand[0])
    player2Cards = getHandCardsDirectory(playerHand[1])
    player3Cards = getHandCardsDirectory(playerHand[2])
    player4Cards = getHandCardsDirectory(playerHand[3])

    if withSpecialCards:
        #If you have two jokers
        if playerHand[0].count(12) == 2:
            #If you are a dishwasher, add the food fight card.
            if roles[0] == 4:
                player1Cards.append("/actionCards/cardFight.png")
            else: #Otherwise add the dinner served card.
                player1Cards.append("/actionCards/cardDinner.png")


    return player1Cards, player2Cards, player3Cards, player4Cards
