from rpython.rlib.parsing.regex import LexingOrExpression

from pie.parsing.deterministic import PieNFA

class PieLexingOrExpression(LexingOrExpression):

    def make_automaton(self):
        dfas = [reg.make_automaton().make_deterministic() for reg in self.regs]
        [dfa.optimize() for dfa in dfas]
        nfas = [dfa.make_nondeterministic() for dfa in dfas]
        result_nfa = PieNFA()
        start_state = result_nfa.add_state(start=True)
        for i, nfa in enumerate(nfas):
            final_state = result_nfa.add_state(self.names[i], final=True,
                                               unmergeable=True)
            state_map = {}
            for j, name in enumerate(nfa.names):
                start = j in nfa.start_states
                final = j in nfa.final_states
                newstate = result_nfa.add_state(name)
                state_map[j] = newstate
                if start:
                    result_nfa.add_transition(start_state, newstate)
                if final:
                    result_nfa.add_transition(newstate, final_state)
            for state, subtransitions in nfa.transitions.iteritems():
                for input, states in subtransitions.iteritems():
                    newstate = state_map[state]
                    newstates = [state_map[s] for s in states]
                    for newtargetstate in newstates:
                        result_nfa.add_transition(
                            newstate, newtargetstate, input)
        return result_nfa
