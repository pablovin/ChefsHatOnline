import numpy
import random
import threading

def updateModel(memory, model, modelDirectory):
    """ Train Q-network on batch sampled from the buffer
            """
    # Sample experience from memory buffer (optionally with PER)

    gamma = 0.95  # discount rate
    random.shuffle(memory)

    s, a, r, d, new_s, possibleActions, newPossibleActions = [], [], [], [], [], [], []
    for m in memory:
        s.append(m.state)
        a.append(m.action)
        r.append(m.reward)
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


class Agent_Embedded():

    def __init__(self, name="NAIVE_RANDOM"):

        self.name = "EMBEDDED_"+name
        self.batchSize = 1

        self.UpdateEveryActions = 5

    def getAction(self,  state, possibleActions, model, trainModel, memory, modelDirectory, ):

        stateVector = numpy.expand_dims(numpy.array(state), 0)

        possibleActionsVector = numpy.expand_dims(numpy.array(possibleActions), 0)
        a = model.predict([stateVector, possibleActionsVector])[0]

        if trainModel and len(memory)>=self.batchSize and len(memory)%self.UpdateEveryActions==0:
            x = threading.Thread(target=updateModel, args=(memory, model, modelDirectory,))
            x.start()

        return a, model





    def actionUpdate(self, memory):

        pass
