"""Pseudocodo for Russel & Norvig Agent Programs"""
from enum import Enum

class Action:
    def run():
        pass

class Rule:
    """just a rule"""
    def get_action() -> Action:
        pass


class State(Enum):
    INITIAL = 0
    RED = 1 
    GREEN = 2
    BLUE = 3

class InputInterpreter:
    """ input interpreter contains the intelligence to map 
        perception to a state.
    """
    def __init__(self, states: list[State]):
        self.states = states

    def interpret(self, percepts: list) -> State:
        """some logic to identify the correct state based on perception"""
        return self.states[-1]

class SimpleReflexAgent:

    def __init__(self, state_rule_pairs: list[(State,Rule)],
                 interpreter: InputInterpreter):
        self.interpreter = interpreter
        self.rule_match = {state: rule for (state, rule) 
                           in state_rule_pairs} # dictionary of state-rule pairs

    def next_action(self, percepts: list) -> Action:
        state = InputInterpreter().interpret(percepts)
        rule = self.rule_match(state)
        action = rule.get_action()
        return action

class WorldModel:
    # a description of how the next state depends on 
    # current state and some taken action
    # dictionary of the world. What may actions do.
    # (state,action) -> next_state
    state_action_state = {}

    def __init__(self, 
                 states: list[State],
                 actions: list[Action]):
        self.states = states
        self.actions = actions

    def get_next_states(self, partial_state):
        # iterate over state action to get the completed states
        possible_states = []
        for action in self.actions:
            possible_states.append(self.state_action_state[(partial_state,action)])
        return possible_states

class ModelBasedAgent:
    MAX_STM_LENGTH = 10

    def __init__(self, world_model: WorldModel,
                 state_rule_pairs: list[(State,Rule)],
                 interpreter: InputInterpreter):
        self.world_model = world_model
        self.interpreter = interpreter
        self.rule_match = {state: rule for (state, rule) 
                           in state_rule_pairs}
        self.short_term_memory =  [State.INITIAL]

    def update_state(self, partial_state: State):
        """uses the world model to update the state"""
        state = self.world_model.get_next_states(partial_state)
        self.short_term_memory.append(state)
        while len(self.short_term_memory) > self.MAX_STM_LENGTH:
            self.short_term_memory = self.short_term_memory[1:] 
        return state

    def next_action(self, percepts: list) -> Action:
        partial_state = InputInterpreter().interpret(percepts)
        state = self.update_state(partial_state)
        rule = self.rule_match(state)
        action = rule.get_action()
        return action 
