import numpy
import random
from SingleGame.Agents import SimilarityNetwork

import threading


def updateModel(memory, model, modelDirectory, rivalry):
    """ Train Q-network on batch sampled from the buffer
            """
    # Sample experience from memory buffer (optionally with PER)

    gamma = 0.95  # discount rate
    random.shuffle(memory)

    s, a, r, d, new_s, possibleActions, newPossibleActions = [], [], [], [], [], [], []
    for m in memory:
        s.append(m.state)
        a.append(m.action)
        r.append(float(m.reward) + rivalry)
        new_s.append(m.next_state)
        possibleActions.append(m.possibleActions)
        newPossibleActions.append(m.new_possibleActions)
        d.append(m.done)

    s = numpy.asarray(s).astype('float32')
    possibleActions = numpy.asarray(possibleActions).astype('float32')
    new_s = numpy.asarray(new_s).astype('float32')
    newPossibleActions = numpy.asarray(newPossibleActions).astype('float32')

    # Apply Bellman Equation on batch samples to train our DDQN
    q = model.predict([s, possibleActions])
    next_q = model.predict([new_s, newPossibleActions])
    q_targ = model.predict([new_s, newPossibleActions])

    s = numpy.array(s)
    a = numpy.array(a)
    r = numpy.array(r)
    d = numpy.array(d)
    q = numpy.array(q)
    possibleActions = numpy.array(possibleActions)

    for i in range(s.shape[0]):
        if bool(d[i]):
            q[i, int(a[i])] = float(r[i])
        else:
            next_best_action = numpy.argmax(next_q[i, :])
            q[i, int(a[i])] = r[i] + gamma * q_targ[i, next_best_action]

    # Train on batch
    history = model.fit([s, possibleActions], q, verbose=False)

    print(" -- "+str(modelDirectory)+" --- Loss:" + str(history.history['loss']))

    model.save(modelDirectory)


class Agent_Embedded_Rivalry():

    def __init__(self, name="EMBEDDED_Rivalry_"):

        self.name = "EMBEDDED_Rivalry_"+name
        self.batchSize = 1
        self.rivalryObservations = 5
        self.UpdateEveryActions=5
        self.gamma = 0.95  # discount rate
        self.personalityPredictor = SimilarityNetwork.SimialrityNetwork()


    def getRivalry(self, observationsHuman, selfObservations, myCompetitiviness, myScore, humanScore):

        if len(observationsHuman) == 0 or len(selfObservations) == 0:
            return 0
        else:
            # print ("My OBS:" + str(self.observationOpponents[myIndex]))
            # print("Opponent OBS:" + str(self.observationOpponents[self.targetOpponent]))

            observationsHuman = observationsHuman[0:self.rivalryObservations]
            selfObservations = selfObservations[0:self.rivalryObservations]
            myCompetitiviness = myCompetitiviness[0:self.rivalryObservations]

            obsMe = []
            for i in selfObservations:
                obsMe.append(i.observation)

            obsHuman = []
            for i in observationsHuman:
                obsHuman.append(i.observationHuman)

            myComp = []
            for i in myCompetitiviness:
                myComp.append(float(i.myCompetitiveness))

            #Obtain the similarity metrics
            # My own DIC
            myDIC = self.personalityPredictor.predict(numpy.array(obsMe))
            myDIC = numpy.swapaxes(myDIC,0,1)
            my_d = numpy.average([numpy.argmax(v) for v in myDIC[:,0]])
            my_i = numpy.average([numpy.argmax(v) for v in myDIC[:, 1]])
            my_c = numpy.average([numpy.argmax(v) for v in myDIC[:, 2]])

            #Target DIC
            targetDIC = self.personalityPredictor.predict(numpy.array(obsHuman))
            targetDIC = numpy.swapaxes(targetDIC,0,1)
            target_d = numpy.average([numpy.argmax(v) for v in targetDIC[:,0]])
            target_i = numpy.average([numpy.argmax(v) for v in targetDIC[:, 1]])
            target_c = numpy.average([numpy.argmax(v) for v in targetDIC[:, 2]])

            #Similarities
            similarities = (numpy.linalg.norm(my_d - target_d) +
                            numpy.linalg.norm(my_i - target_i) +
                            numpy.linalg.norm(my_c - target_c))/3


            similarities = numpy.average(similarities)
            # print("my_d: " + str(my_d))
            # print("target_d: " + str(target_d))


            #Competitivenes
            competitiveness = numpy.average(myComp)

            competitiveness = numpy.average(competitiveness)
            #Relative Performance
            myPoints = myScore
            targetPoints = humanScore  if humanScore  > 0 else 0.00001
            relativePerformance = float(100 * float(myPoints) / float(targetPoints)) / 100

            #Rivalry
            rivalry = (similarities+competitiveness+relativePerformance)/3
            if rivalry> 1:
                rivalry=1

            return rivalry

    def getConfidence(self, qValue):

        confidences = []
        for v in qValue:

            maxreward = 1
            theta = 0.0
            # maxreward = 0.1
            probability = (1 - theta) * (1 / 2 * numpy.log10(v / maxreward) + 1)

            probability = numpy.tanh(probability)

            if probability <= 0:
                probability = 0
            if probability >= 1:
                probability = 1
            confidences.append(probability)

        probability = numpy.sum(confidences)

        return probability

    def getAction(self,  state, possibleActions, model, trainModel, memory, modelDirectory, observationsHuman, selfObservations, myCompetitiviness, myScore, humanScore ):

        stateVector = numpy.expand_dims(numpy.array(state), 0)

        possibleActionsVector = numpy.expand_dims(numpy.array(possibleActions), 0)

        a = model.predict([stateVector, possibleActionsVector])[0]

        if trainModel and len(memory)>=self.batchSize and len(memory)%self.UpdateEveryActions==0:
            rivalry = self.getRivalry(observationsHuman, selfObservations, myCompetitiviness, myScore, humanScore)
            x = threading.Thread(target=updateModel, args=(memory, model, modelDirectory,rivalry,))
            x.start()
        else:
            rivalry = -1

        confidences = self.getConfidence(a)

        return a, model, confidences, rivalry







    def actionUpdate(self, memory):

        pass
