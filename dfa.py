import node, nfa

class DFA:
    def __init__(self, inp: nfa.NFA):
        self.dfa = None
        self.inp = inp
    
    def createDFA(self) -> node.Node:
        nodes = {}
        eps_n = {}
        found = set([])
        head = self.inp.stack[0]
        temp = head
        head = self.findEpsilon(head)
        head.add(self.inp.stack[0])
        eps_n[temp] = head
        found.add(frozenset(head))
        nodes[frozenset(head)] = node.createNode()
        nodes[frozenset(set([]))] = node.createNode()
        for n in head:
            if n.accepting:
                nodes[frozenset(head)].isAccepting(True)
                break

        while found:
            p_node = found.pop()
            for ch in self.inp.alpha:
                next_nodes = set([])
                for n in p_node:
                    if ch in n.transitions:
                        for ns in n.transitions[ch]:
                            if not ns in eps_n:
                                eps_n[ns] = self.findEpsilon(ns)
                                eps_n[ns].add(ns)
                            next_nodes.update(eps_n[ns])

                if not frozenset(next_nodes) in nodes:
                    nodes[frozenset(next_nodes)] = node.createNode()
                    for n in next_nodes:
                        if n.accepting:
                            nodes[frozenset(next_nodes)].isAccepting(True)
                    found.add(frozenset(next_nodes))
                nodes[p_node].addTransition(ch, nodes[frozenset(next_nodes)])
        for ch in self.inp.alpha:
            nodes[frozenset(set([]))].addTransition(ch, nodes[frozenset(set([]))])
        return nodes[frozenset(head)]
                
                
    def findEpsilon(self, n : node.Node, vis = None):
        if vis is None:
            vis = set([])
        vis.add(n)
        neigh = set([])
        for x, y1 in n.transitions.items():
            for y in y1:
                if x == "":
                    neigh.add(y)
                    if not y in vis:
                        vis.add(y)
                        neigh.update(self.findEpsilon(y, vis))
        return neigh

    def readDFA(self, s: str, n: node.Node, x: int) -> bool:
        if x == len(s):
            return n.accepting
        if s[x] in n.transitions:
            return self.readDFA(s, n.transitions[s[x]][0], x+1)
        else:
            return False
            

def print_dfa(start):
    state_id = {}

    queue = [start]
    count = 0

    while queue:
        curr = queue.pop(0)

        if curr not in state_id:
            state_id[curr] = count
            count += 1

        for destinations in curr.transitions.values():
            for dest in destinations:
                if dest not in state_id:
                    state_id[dest] = count
                    count += 1
                    queue.append(dest)

    alphabet = set()

    for curr in state_id:
        for ch in curr.transitions:
            if ch != "":
                alphabet.add(ch)

    alphabet = sorted(alphabet)

    print("State", *alphabet, sep=", ")

    for curr, num in state_id.items():
        prefix = ""

        if curr is start:
            prefix = "->"

        if curr.accepting:
            prefix += "*"

        row = [prefix + str(num)]

        for ch in alphabet:
            if ch in curr.transitions and curr.transitions[ch]:
                dest = curr.transitions[ch][0]
                row.append(str(state_id[dest]))
            else:
                row.append("-")

        print(*row, sep=", ")