class Node:
    def __init__(self, transitions, accepting):
        self.transitions: dict = transitions
        self.accepting : bool = accepting

    def isAccepting(self, x):
        self.accepting = x

    def addTransition(self, ch: str, node: Node):
        if ch in self.transitions:
            self.transitions[ch].append(node)
        else:
            self.transitions[ch] = []
            self.transitions[ch].append(node)

def createNode():
    return Node({}, False)