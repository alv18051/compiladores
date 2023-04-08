class AFNSimulation():

    def __init__(self, afn, string):
        self.afn = afn
        self.string = string+'$'
        self.actualIndex = 0
        self.eof = self.string[-1]
        self.eClosures = []

    def simulate(self):
        S = self.subsets(
            self.afn.initial_state, self.afn.initial_state)
        nextC = self.nextC()
        while nextC != self.eof:
            self.eClosures = []
            move = self.moves(S, nextC)
            S = self.subsets(move, move)
            nextC = self.nextC()

        if self.afn.final_state in S:
            return True

        return False

    def nextC(self):
        nextC = self.string[self.actualIndex]

        self.actualIndex += 1

        return nextC


    def subsets(self, estados, ogState):

        if isinstance(estados, int):
            estados = [estados]
        if isinstance(ogState, int):
            ogState = [ogState]

        for estado in estados:
            if estado not in self.eClosures:
                self.eClosures.append(estado)
            for transicion in self.afn.transitions:
                if transicion.state == estado:
                    if transicion.symbol == 'ε':
                        if transicion.next_state not in self.eClosures:
                            self.eClosures.append(transicion.next_state)
                            self.subsets(transicion.next_state, ogState)

        return self.eClosures


    def moves(self, states, char):

        otherEClosures = []

        for state in states:
            for transition in self.afn.transitions:
                if transition.state == state and transition.symbol == char:
                    otherEClosures.append(transition.next_state)

        return otherEClosures


class AFDSimulation():

    def __init__(self, afd, string):
        self.afd = afd
        self.string = string
        self.actualIndex = 0
        self.eof = self.string[-1]


    def simulate(self):
        currentState = self.afd.initial_state
        for symbol in self.string:
            nexState = None
            for transition in self.afd.transitions:
                if transition.state == currentState and transition.symbol == symbol:
                    nexState = transition.next_state
                    break
            if nexState == None:
                return False
            currentState = nexState

        if currentState in self.afd.final_states:
            return True
        return False