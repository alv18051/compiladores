import graphviz as gv

class DrawAF:
    

    def __init__(self, transitions, initial_state, final_states, title="Automata"):
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.graph = gv.Digraph(graph_attr={'rankdir': 'LR'})

        for transition in self.transitions:
            self.graph.edge(str(transition.state), str(
                transition.next_state), label=transition.symbol)

        self.graph.node(str(initial_state), shape='circle', style='bold')
        self.graph.node('start', shape='point')
        self.graph.edge('start', str(initial_state), arrowhead='normal')

        for final_state in final_states:
            self.graph.node(str(final_state), shape='doublecircle')

        if title:
            self.graph.node('title', label=title, shape='none',
                        fontsize='20', fontcolor='black', fontname='Arial')


    def draw(self, filename='my_nfa'):
        return self.graph.view(filename=filename)