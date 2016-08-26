class Criteria():
    Type = {'Entropy': 1, 'Gini': 2}

class Gain():
    Type = {'InfoGain': 1, 'GainRatio': 2}

class Algo:
    def __init__(self, gain, criteria):
        self.gain = Gain.Type[gain]
        self.criteria = Criteria.Type[criteria]
