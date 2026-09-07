import node
class NFA:
    def __init__(self, reg):
        self.stack = []
        self.regex = reg
        self.alpha = set([])

    def read(self):
        for s in self.regex:
            if s == '|':
                if self.union() == -1:
                    return -1
            elif s == ".":
                if self.dot() == -1:
                    return -1
            elif s == '*':
                if self.star() == -1:
                    return -1
            elif s == '+':
                if self.plus() == -1:
                    return -1
            elif s == '?':
                if self.ques() == -1:
                    return -1
            elif s[0] == '\\':
                if self.char(s[1]) == -1:
                    return -1
            elif s[0] == '[':
                if self.rangeChar(s) == -1:
                    return -1
            elif s == "(":
                self.stack.append(s)
            elif s == ")":
                if self.bracket() == -1:
                    return -1
            else:
                if self.char(s) == -1:
                    return -1


        l = len(self.stack)
        #print("Length of Stack =", l)
        x = 0
        while x < l-1:
            self.stack[x][1].addTransition("", self.stack[x+1][0])
            self.stack[x][1].isAccepting(False)
            x = x+1
        self.stack = [self.stack[0][0], self.stack[l-1][1]].copy()    
        return 0   

    def dot(self):
        if len(self.stack) >= 2:
            a = self.stack.pop()
            b = self.stack.pop()
            b[1].addTransition("", a[0])
            b[1].isAccepting(False)
            a[1].isAccepting(True)
            self.stack.append([b[0], a[1]])
            return 0
        return -1

    def char(self, s):
        n = node.createNode()
        f = node.createNode()
        n.addTransition(s, f)
        f.isAccepting(True)
        self.stack.append([n, f])
        self.alpha.add(s)
        return 0

    def union(self):
        if len(self.stack) >= 2:
            n = node.createNode()
            f = node.createNode()
            a = self.stack.pop()
            b = self.stack.pop()
            n.addTransition("", a[0])
            a[1].addTransition("", f)
            a[1].isAccepting(False)
            n.addTransition("", b[0])
            b[1].addTransition("", f)
            b[1].isAccepting(False)
            f.isAccepting(True)
            self.stack.append([n, f])
            return 0
        else:
            return -1

    def star(self):
        if len(self.stack) >= 1:
            n = node.createNode()
            f = node.createNode()
            a = self.stack.pop()
            n.addTransition("", a[0])
            n.addTransition("", f)
            a[1].isAccepting(False)
            a[1].addTransition("", n)
            a[1].addTransition("", f)
            f.isAccepting(True)
            self.stack.append([n, f])
            return 0
        else:
            return -1

    def plus(self):
        if len(self.stack) >= 1:
            n = node.createNode()
            f = node.createNode()
            a = self.stack.pop()
            n.addTransition("", a[0])
            a[1].isAccepting(False)
            a[1].addTransition("", n)
            a[1].addTransition("", f)
            f.isAccepting(True)
            self.stack.append([n, f])
            return 0
        else:
            return -1

    def ques(self):
        if len(self.stack) >= 1:
            n = node.createNode()
            f = node.createNode()
            a = self.stack.pop()
            n.addTransition("", a[0])
            n.addTransition("", f)
            a[1].addTransition("", f)
            a[1].isAccepting(False)
            f.isAccepting(True)
            self.stack.append([n, f])
            return 0
        else:
            return -1

    def rangeChar(self, s):
        n = node.createNode()
        f = node.createNode()
        if s[2] == '-':
            if len(s) > 5:
                return -1
            ch1 = s[1]
            ch2 = s[3]
            for x in range(ord(ch1), ord(ch2)+1):
                n.addTransition(chr(x), f)
                self.alpha.add(chr(x))
            f.isAccepting(True)
            self.stack.append([n,f])
            return 0
        else:
            x = 1
            l = len(s)
            while x < l-1:
                n.addTransition(s[x], f)
                self.alpha.add(s[x])
            f.isAccepting(True)
            self.stack.append([n, f])
            return 0

    def bracket(self):
        nodes = []
        while self.stack:
            n = self.stack.pop()
            nodes.append(n)
            if(n == "("):
                break
        if nodes[-1] == "(":
            nodes = nodes[:-1]
            nodes.reverse()
            l = len(nodes)
            x = 0
            while x < l-1:
                nodes[x][1].addTransition("", nodes[x+1][0])
                nodes[x][1].isAccepting(False)
                x = x+1
            self.stack.append([nodes[0][0], nodes[l-1][1]])
            return 0
        else:
            return -1

def print_nfa(start, final):
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

    print("\n========== NFA ==========\n")

    for curr, num in state_id.items():

        if curr is start and curr is final:
            state_type = " [START, FINAL]"
        elif curr is start:
            state_type = " [START]"
        elif curr is final:
            state_type = " [FINAL]"
        else:
            state_type = ""

        print(f"Node {num}{state_type}")
        print(f"  Accepting: {curr.accepting}")

        if not curr.transitions:
            print("  No transitions")

        for ch, destinations in curr.transitions.items():
            label = "ε" if ch == "" else ch

            for dest in destinations:
                print(f"  --{label}--> Node {state_id[dest]}")

        print()

    print("==========================")
    print(f"Total states: {count}")
    print("==========================\n")

