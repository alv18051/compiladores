class Transition:

    def __init__(self, state, symbol, next_state):
        self.state = state
        self.symbol = symbol
        self.next_state = next_state

    def __str__(self):
        return f"[State: {self.state}, Symbol: {self.symbol}, NextState: {self.next_state}]"

    def print_transition(self):
        print(
            f"[State: {self.state}, Symbol: {self.symbol}, NextState: {self.next_state}]")


class AFN:

    def __init__(self, initial_state, final_state):
        self.transitions = []
        self.initial_state = initial_state
        self.final_state = final_state
        self.states = []


    def getStates(self):
        states = []


        for transition in self.transitions:
            if transition.state not in states:
                states.append(transition.state)
            if transition.next_state not in states:
                states.append(transition.next_state)
        self.states = sorted(states)

    def print_dfa(self):
        print("AFN")
        print(f"Estado inicial: {self.initial_state}")
        print(f"Estado final: {self.final_state}")
        print("Numero de transiciones: ", len(self.transitions))


class AFD:
    def __init__(self, initial_state, final_states):
        self.transitions = []
        self.initial_state = initial_state
        self.final_states = final_states
        self.states = []

    def getStates(self):
        states = []

        for transition in self.transitions:
            if transition.state not in states:
                states.append(transition.state)
            if transition.next_state not in states:
                states.append(transition.next_state)

        self.states = sorted(states)

    def print_afd(self):
        print("AFD")
        print("Transiciones AFD:")
        for transition in self.transitions:
            print(
                f"[{transition.state}, {transition.symbol}, {transition.next_state}]")
        print(f"- Estado Inicial: {self.initial_state}")
        print(f"- Estados Finales: {self.final_states}")
        estados = []
        for transition in self.transitions:
            if transition.state not in estados:
                estados.append(transition.state)
            if transition.next_state not in estados:
                estados.append(transition.next_state)
        print(f"- Numero de estados: {len(estados)}")
        