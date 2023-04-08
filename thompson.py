from afdAFN import *

class Thompson:
    def __init__(self, postfix):
        self.postfix = postfix
        self.generated_states = 0

    def rules(self, symbol):
        state = self.generated_states
        self.generated_states += 1

        next_state = self.generated_states
        self.generated_states += 1

        nfa = AFN(state, next_state)
        transition = Transition(state, symbol, next_state)
        nfa.transitions.append(transition)

        return nfa
    
    def orExp(self, nfa1, nfa2):
        initial_state = self.generated_states
        state1 = self.generated_states
        self.generated_states += 1

        final_state = self.generated_states
        state2 = self.generated_states
        self.generated_states += 1

        afn = AFN(initial_state, final_state)
        transition1 = Transition(state1, 'ε', nfa1.initial_state)
        transition2 = Transition(state1, 'ε', nfa2.initial_state)
        transition3 = Transition(nfa1.final_state, 'ε', state2)
        transition4 = Transition(nfa2.final_state, 'ε', state2)

        afn.transitions.append(transition1)
        afn.transitions.append(transition2)

        for transition in nfa1.transitions:
            afn.transitions.append(transition)
        for transition in nfa2.transitions:
            afn.transitions.append(transition)

        afn.transitions.append(transition3)
        afn.transitions.append(transition4)

        return afn
    
    def kleeneStar(self, afn):
        initial_state = self.generated_states
        self.generated_states += 1

        final_state = self.generated_states
        self.generated_states += 1

        nfa = AFN(initial_state, final_state)

        transition1 = Transition(initial_state, 'ε', afn.initial_state)
        nfa.transitions.append(transition1)

        for transition in afn.transitions:
            nfa.transitions.append(transition)

        transition2 = Transition(nfa.final_state, 'ε', afn.initial_state)
        transition3 = Transition(afn.final_state, 'ε', final_state)
        transition4 = Transition(initial_state, 'ε', final_state)

        nfa.transitions.append(transition2)
        nfa.transitions.append(transition3)
        nfa.transitions.append(transition4)

        return nfa
    
    def concatExp(self, nfa1, nfa2):
        nfa = AFN(nfa1.initial_state, nfa2.final_state)

        for transition in nfa1.transitions:
            nfa.transitions.append(transition)

        final_nfa1 = nfa1.final_state
        initial_nfa2 = nfa2.initial_state

        for transition in nfa2.transitions:
            if transition.state == initial_nfa2:
                transition.state = final_nfa1

        for transition in nfa2.transitions:
            nfa.transitions.append(transition)

        return nfa
    def nfaConstruction(self):

        stack = []

        for i in range(len(self.postfix)):
            character = self.postfix[i]

            if character not in ['|', '.', '*']:
                stack.append(self.rules(character))
            else:
                if character == '|':
                    nfa2 = stack.pop()
                    nfa1 = stack.pop()
                    stack.append(self.orExp(nfa1, nfa2))

                if character == '.':
                    nfa2 = stack.pop()
                    nfa1 = stack.pop()
                    stack.append(self.concatExp(nfa1, nfa2))

                if character == '*':
                    nfa1 = stack.pop()
                    stack.append(self.kleeneStar(nfa1))

        return stack[-1]

    