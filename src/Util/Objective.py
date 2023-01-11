class Objective:
    def __init__(self, start_state, goal_state, observation_top, observation_width, observation_height, labels = [], avoid_labels = []):
        self.start_state = start_state
        self.goal_state = goal_state
        self.labels = labels
        self.avoid_labels = avoid_labels
        self.observation_top = observation_top
        self.observation_width = observation_width
        self.observation_height = observation_height

    def to_string(self):
        return "(" + str(self.start_state) + ", " + str(self.goal_state) + ")"