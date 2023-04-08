from afdAFN import *

class Subsets:

    def __init__(self, afn):
        self.afn = afn
        self.afnTransitions = afn.transitions
        self.afnInitialState = afn.initial_state
        self.nfaFinalState = afn.final_state
        self.generated_states = 0
        self.symbolsList = self.symbols()
        self.afdTransitions = {}
        self.stateSubsets = {}
        self.visited = [[self.afnInitialState]]
        self.eClosures = []

    def symbols(self):
        symbol = []
        for transition in self.afnTransitions:
            if transition.symbol not in symbol and transition.symbol != 'ε':
                symbol.append(transition.symbol)
        return symbol

    def subsets(self, estados, ogState):
        if isinstance(estados, int):
            estados = [estados]
        if isinstance(ogState, int):
            ogState = [ogState]

        for estado in estados:
            if estado not in self.eClosures:
                self.eClosures.append(estado)
            for transicion in self.afnTransitions:
                if transicion.state == estado:
                    if transicion.symbol == 'ε':
                        if transicion.next_state not in self.eClosures:
                            self.eClosures.append(transicion.next_state)
                            self.subsets(transicion.next_state, ogState)

        self.stateSubsets[tuple(ogState)] = self.eClosures

        return self.eClosures

    def moves(self, eclosure):
        eclosureCopy = eclosure.copy()
        self.eClosures = []
        tempDic = {}
        for symbol in self.symbolsList:
            next_states = []
            for estado in eclosureCopy:
                for transicion in self.afnTransitions:
                    if transicion.state == estado and transicion.symbol == symbol:
                        next_states.append(transicion.next_state)
                if symbol == '' and estado in next_states:
                    next_states.remove(estado)
                    next_states.extend(self.eclosure(estado))
            if len(next_states) == 0:
                next_states.append(None)
            tempDic[symbol] = list(set(next_states))

        for k, v in self.stateSubsets.items():
            if v == eclosureCopy:
                self.afdTransitions[k] = tempDic
        for k, v in tempDic.items():
            if v != [None]:
                if v not in self.visited:
                    self.visited.append(v)

        return tempDic

    def afdAddTransitions(self, estado):
        self.subsets(estado, estado)

        dic = self.moves(self.eClosures)
        for k, v in dic.items():

            if v in self.visited and tuple(v) not in self.afdTransitions:
                self.afdAddTransitions(v)

    def subAFDConstruction(self):

        self.afdAddTransitions(self.afnInitialState)

        sorted_afdTransitions = {}
        subsets = self.stateSubsets.copy()

        for key, value in self.afdTransitions.items():
            sorted_key = tuple(sorted(key))
            sorted_value = {}
            for k, v in value.items():
                sorted_value[k] = sorted(list(set(v)))
            sorted_afdTransitions[sorted_key] = sorted_value

        asignState = {i: key for i, key in enumerate(subsets)}

        new_dict = {}
        for key, value in asignState.items():
            sorted_value = tuple(sorted(value))
            if sorted_value not in new_dict.values():

                new_dict[key] = sorted_value

        afdInitial = 0
        afdFinals = []
        dfa = AFD(afdInitial, afdFinals)

        for key, value in sorted_afdTransitions.items():
            for k, v in value.items():
                if v != [None]:
                    v = tuple(v)
                    for i, j in new_dict.items():
                        sortedJ = tuple(sorted(j))
                        if j == v or sortedJ == v:
                            v = i
                        if j == key or sortedJ == key:
                            key = i
                    transition = Transition(key, k, v)
                    dfa.transitions.append(transition)

        for i, j in self.stateSubsets.items():
            if self.nfaFinalState in j:
                for x, y in new_dict.items():
                    sortedI = tuple(sorted(i))
                    if y == i or y == sortedI:
                        state = x
                        dfa.final_states.append(state)
        dfa.final_states = list(set(dfa.final_states))
        dfa.getStates()

        return dfa