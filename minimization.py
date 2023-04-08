from afdAFN import *

class Minimization():

    def __init__(self, afd):
        self.afd = afd
        self.afdFinalStates = afd.final_states
        self.afdStates = afd.states
        self.afdTransitions = afd.transitions
        self.initialPartition = []
        self.partitions = []
        self.symbolsList = self.symbols()
        self.transitions = {}
        self.finalStates = []
        self.initialState = 0

    def symbols(self):
        symbol = []
        for transition in self.afdTransitions:
            if transition.symbol not in symbol:
                symbol.append(transition.symbol)
        return symbol

    def buildInitialPartition(self):
        accept = []
        accept.extend(self.afdFinalStates)

        nonAccept = []

        for state in self.afdStates:
            if state not in accept:
                nonAccept.append(state)

        self.initialPartition.append(accept)

        if nonAccept:
            self.initialPartition.append(nonAccept)

        self.buildNewPartitions(self.initialPartition)


    def buildNewPartitions(self, partitions):

        self.partitions = partitions.copy()
        newPartitions = self.partitions.copy()

        for partition in self.partitions:
            dicPartition = {}
            if len(partition) > 1:
                for state in partition:
                    dicSymbol = {}
                    for symbol in self.symbolsList:
                        for transition in self.afdTransitions:
                            if transition.state == state and transition.symbol == symbol:
                                dicSymbol["G"+symbol] = "G" + str(
                                    self.getIndex(
                                        transition.next_state, self.partitions))
                    dicPartition[state] = dicSymbol   
                index = newPartitions.index(partition)
                newPartitions.pop(index)
                for i, l in enumerate(self.getCombinations(dicPartition)):
                    newPartitions.insert(index + i, l)

        if newPartitions == self.partitions:
            return self.partitions

        self.buildNewPartitions(newPartitions)

    def getIndex(self, integer, list):
        for i, sublist in enumerate(list):
            if integer in sublist:
                return i


    def getCombinations(self, dicPartition):
        result = []
        value_sets = set()
        value_dict = {}

        for key, values in dicPartition.items():
            value_set = frozenset(values.items())
            if value_set not in value_sets:
                value_sets.add(value_set)
                value_dict[value_set] = [key]
            else:
                value_dict[value_set].append(key)

        for key_set, keys in value_dict.items():
            result.append(keys)

        return result

    def minAFDConstruction(self):

        self.buildInitialPartition()
        self.partitions = sorted(self.partitions, key=lambda x: x[0])
        for partition in self.partitions:
            for state in self.afdFinalStates:
                if state in partition:
                    estadoNuevo = self.getIndex(state, self.partitions)
                    self.finalStates.append(estadoNuevo)

        self.finalStates = list(set(self.finalStates))

        dfa = AFD(self.initialState, self.finalStates)

        for partition in self.partitions:
            representative = partition[0]
            index = self.getIndex(representative, self.partitions)
            dicSymbol = {}
            for symbol in self.symbolsList:
                for transition in self.afdTransitions:
                    if transition.state == representative and transition.symbol == symbol:
                        nextIndex = self.getIndex(
                            transition.next_state, self.partitions)
                        dicSymbol[symbol] = nextIndex
                        transition = Transition(index, symbol, nextIndex)
                        dfa.transitions.append(transition)
            self.transitions[index] = dicSymbol

        return dfa


