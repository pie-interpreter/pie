from pypy.rlib.parsing.deterministic import DFA, NFA, compress_char_set
from pypy.rlib.parsing.codebuilder import Codebuilder
import py

class PieDFA(DFA):

    def make_lexing_code(self):
        result = Codebuilder()
        result.start_block("def recognize(runner, i):")
        result.emit("#auto-generated code, don't edit")
        result.emit("assert i >= 0")

        # NOTE: Changes for pie:
        #       All the copying is done for the next line - all the text, that
        #       is beeing parsed for tokens is converted to lower case, so that
        #       all tokens would determined without taking their case in the
        #       account. Token sources in the result will keep their case. The
        #       only disadvantage in this is that we won't be able to differ two
        #       tokens, based only on their case.
        result.emit("input = runner.text.lower()")
        result.emit("state = 0")
        result.start_block("while 1:")
        state_to_chars = {}
        for (state, char), nextstate in self.transitions.iteritems():
            state_to_chars.setdefault(state, {}).setdefault(nextstate, set()).add(char)
        state_to_chars_sorted = state_to_chars.items()
        state_to_chars_sorted.sort()
        above = set()
        for state, nextstates in state_to_chars_sorted:
            above.add(state)
            with result.block("if state == %s:" % (state, )):
                if state in self.final_states:
                    result.emit("runner.last_matched_index = i - 1")
                    result.emit("runner.last_matched_state = state")
                with result.block("try:"):
                    result.emit("char = input[i]")
                    result.emit("i += 1")
                with result.block("except IndexError:"):
                    result.emit("runner.state = %s" % (state, ))
                    if state in self.final_states:
                        result.emit("return i")
                    else:
                        result.emit("return ~i")
                elif_prefix = ""
                for nextstate, chars in nextstates.iteritems():
                    final = nextstate in self.final_states
                    compressed = compress_char_set(chars)
                    if nextstate in above:
                        continue_prefix = "continue"
                    else:
                        continue_prefix = ""
                    for i, (a, num) in enumerate(compressed):
                        if num < 3:
                            for charord in range(ord(a), ord(a) + num):
                                with result.block("%sif char == %r:"
                                        % (elif_prefix, chr(charord))):
                                    result.emit("state = %s" % (nextstate, ))
                                    result.emit(continue_prefix)
                                if not elif_prefix:
                                    elif_prefix = "el"
                        else:
                            with result.block(
                                "%sif %r <= char <= %r:" % (
                                    elif_prefix, a, chr(ord(a) + num - 1))):
                                    result.emit("state = %s" % (nextstate, ))
                                    result.emit(continue_prefix)
                            if not elif_prefix:
                                elif_prefix = "el"
                with result.block("else:"):
                    result.emit("break")
        #print state_to_chars.keys()
        for state in range(self.num_states):
            if state in state_to_chars:
                continue
            assert state in self.final_states
        result.emit("""
runner.last_matched_state = state
runner.last_matched_index = i - 1
runner.state = state
if i == len(input):
    return i
else:
    return ~i
break""")
        result.end_block("while")
        result.emit("""
runner.state = state
return ~i""")
        result.end_block("def")
        result = result.get_code()
        while "\n\n" in result:
            result = result.replace("\n\n", "\n")
        #print result
        exec py.code.Source(result).compile()

        return recognize


class PieNFA(NFA):

    def make_deterministic(self, name_precedence=None):
        fda = PieDFA()
        set_to_state = {}
        stack = []
        def get_dfa_state(states):
            states = self.epsilon_closure(states)
            frozenstates = frozenset(states)
            if frozenstates in set_to_state:
                return set_to_state[frozenstates]   # already created this state
            if states == self.start_states:
                assert not set_to_state
            final = bool(
                filter(None, [state in self.final_states for state in states]))
            name = ", ".join([self.names[state] for state in states])
            if name_precedence is not None:
                name_index = len(name_precedence)
            unmergeable = False
            for state in states:
                if state in self.unmergeable_states:
                    new_name = self.names[state]
                    if name_precedence is not None:
                        try:
                            index = name_precedence.index(new_name)
                        except ValueError:
                            index = name_index
                        if index < name_index:
                            name_index = index
                            name = new_name
                    else:
                        name = new_name
                    unmergeable = True
            result = set_to_state[frozenstates] = fda.add_state(
                name, final, unmergeable)
            stack.append((result, states))
            return result
        startstate = get_dfa_state(self.start_states)
        while stack:
            fdastate, ndastates = stack.pop()
            chars_to_states = {}
            for state in ndastates:
                sub_transitions = self.transitions.get(state, {})
                for char, next_states in sub_transitions.iteritems():
                    chars_to_states.setdefault(char, set()).update(next_states)
            for char, states in chars_to_states.iteritems():
                if char is None:
                    continue
                fda[fdastate, char] = get_dfa_state(states)
        return fda
